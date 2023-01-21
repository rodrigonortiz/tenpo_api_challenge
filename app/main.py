#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exception_handler import validation_exception_handler, python_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, status
from fastapi.logger import logger
from predict import predict
from config import CONFIG
from joblib import load
from schema import *
import traceback
import uvicorn
import torch
import os
import sys



# Inicializa el servidor API
app = FastAPI(
    title="Tenpo API challenge",
    description="Multiplication of a tensor by 2",
    version="0.0.1"
)


# Integra excepciones customizadas
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, python_exception_handler)


# Evento que se ejecuta cuando la API se inicializa
@app.on_event("startup")
async def startup_event():
    """
    Inicializar API y sus variables
    """

    logger.info('Running envirnoment: {}'.format(CONFIG['ENV']))

    # Cargar modelo
    model = torch.jit.load(CONFIG['MODEL_PATH'])

    # Insertar el modelo en el estado de la app
    app.package = {
        "model": model
    }


# Endpoint principal
@app.post('/api/predict/',
          response_model=InferenceResponse,
          responses={422: {"model": ErrorResponse},
                     500: {"model": ErrorResponse}}
          )
def make_predict(request: Request, body: InferenceInput):
    """
    Generar prediccion en base a los datos de entrada
    """

    logger.info('API predict endpoint called')
    logger.info(f'input: {body}')

    # Convertir Lista en Tensor
    new_tensor = torch.tensor(body.values_list)

    # Generar prediccion
    tensor_by_2 = predict(app.package, new_tensor)

    # Convertir tensor a lista para output
    tensor_by_2_list = tensor_by_2.tolist()

    # Convertir resultado a json
    result = {'tensor_by_2': tensor_by_2_list}

    logger.info(f'result: {result}')

    return {
        "error": False,
        "results": result
    }



if __name__ == '__main__':
    # server api
    uvicorn.run("main:app", host="127.0.0.1", port=8080,
                reload=True, log_config="log.ini"
                )