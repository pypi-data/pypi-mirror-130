from __future__ import annotations

import json

from typing import Callable, Dict
from breath_api_interface.proxy import ServiceProxy
from breath_api_interface.queue import Queue
from breath_api_interface.request import Request, Response
from breath_api_interface.service_interface import Service

import numpy as np
import tensorflow as tf
from tensorflow import keras

import traceback

features = np.asarray(["Precipitacao", 
            "Pressao_at_max", 
            "Pressao_at_min",
            "Radiacao",	
            "Temp_max",	
            "Temp_min",	
            "Umidade",	
            "Max_vent",	
            "Velocidade_vent",	
            "Pop_estimada"])

class Prediction(Service):
    def __init__(self, proxy: ServiceProxy, request_queue: Queue, global_response_queue: Queue):
        
        super().__init__(proxy, request_queue, global_response_queue, "Prediction")

        self._operations : Dict[str, Callable[[Prediction, Request], Response]] = {
            "predict": self._predict,
        }

        self._model = None
        self._train_dist = None
        self._target_dist = None

    def run(self) -> None:
        '''Run the service, handling BD requests.
		'''
        request = self._get_request()

        if request is None:
            return

        response : Response = request.create_response(sucess=False, response_data={"message": "Operation not available"})

        if request.operation_name in self._operations:
            response = self._operations[request.operation_name](request)

        self._send_response(response)

    def _load_model(self):
        if self._model is not None:
            return

        response = self._send_request("DataWorkflow", "run_workflow", request_info={"workflow_name":"ModelDownloader"})

        if response.sucess == True:
            self._model = keras.models.load_model("model.h5")

            file = open("train_dist.json", "r")
            self._train_dist = json.load(file)
            file.close()

            file = open("target_dist.json", "r")
            self._target_dist = json.load(file)
            file.close()
        else:
            print("LOG: Erro - Não foi possível carregar o modelo.")
            raise RuntimeError("Não foi possível carregar o modelo")

    def _predict(self, request:Request) -> Response:
        self._load_model()

        x = np.ones(len(features), dtype=np.float32) * np.inf


        for index in range(len(features)):
            name = features[index]
            if name in request.request_info:
                x[index] = request.request_info[name]
                x[index] = (x[index]*self._train_dist[name]["std"])+self._train_dist[name]["mean"]

        if (x == np.inf).sum() != 0:
            return request.create_response(False, {"message":"Missing feature to prediction"})        

        x = x.reshape(-1, 10)

        y = self._model.predict(x).flatten()[0]

        y = (y*self._target_dist["std"])+self._target_dist["mean"]

        response = request.create_response(True, {"prediction": y})

        return response