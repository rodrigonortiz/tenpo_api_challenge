#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exception_handler import validation_exception_handler, python_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, status
from fastapi.logger import logger
from joblib import load
from predict import predict
from config import CONFIG
from schema import *
import torch



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

    # Cargar modelo (en el caso de tener uno se carga aca)
    #model = torch.jit.load(CONFIG['MODEL_PATH'])

    # Insertar el modelo en el estado de la app
    """
    app.package = {
        "model": model
    }
    """


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
    tensor_by_2 = predict(new_tensor)

    # Convertir tensor a lista para output
    tensor_by_2_list = tensor_by_2.tolist()

    # Convertir resultado a json
    result = {'tensor_list': tensor_by_2_list}

    logger.info(f'result: {result}')

    return {
        "error": False,
        "result": result
    }
