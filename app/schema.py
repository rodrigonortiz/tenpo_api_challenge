#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import torch



class InferenceInput(BaseModel):
    """
    Valores del input para realizar la inferencia
    """
    values_list: list[int]



class InferenceResult(BaseModel):
    """
    Resultado de la inferencia
    """
    tensor_list: list 



class InferenceResponse(BaseModel):
    """
    Respuesta del modelo
    """
    error: bool
    result: InferenceResult



class ErrorResponse(BaseModel):
    """
    Respuesta de error en llamada a la API
    """
    error: bool
    message: str