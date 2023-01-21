#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.logger import logger
from fastapi import Request, status
from config import CONFIG
import traceback
import json


def get_error_response(request, exc) -> dict:
    """
    Manejo de errores genericos
    """

    error_response = {
        "error": True,
        "message": str(exc)
    }

    # Retornar el traceback info si esta en modo debugueo
    if CONFIG['DEBUG']:
        error_response["traceback"] = "".join(
            traceback.format_exception(
                etype=type(exc), value=exc, tb=exc.__traceback__
            )
        )

    return error_response


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Manejo de error en la request
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=get_error_response(request, exc)
    )


async def python_exception_handler(request: Request, exc: Exception):
    """
    menejo de cualquier error interno
    """

    # Log requester infomation
    logger.error('Request info:\n' + json.dumps({
        "host": request.client.host,
        "method": request.method,
        "url": str(request.url),
        "headers": str(request.headers),
        "path_params": str(request.path_params),
        "query_params": str(request.query_params),
        "cookies": str(request.cookies)
    }, indent=4))

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=get_error_response(request, exc)
    )