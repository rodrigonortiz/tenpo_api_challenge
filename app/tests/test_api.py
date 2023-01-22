#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from ..main import app
import uvicorn
import pytest


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

#Test basico de respues de la API
def test_main_predict(client):
    """
    Test respuesta prediccion
    """

    headers = {}
    body = {
        "values_list": [1,2,3,4]
    }

    response = client.post("/api/predict",
                           headers=headers,
                           json=body)

    try:
        assert response.status_code == 200
        reponse_json = response.json()
        assert reponse_json['error'] == False
        assert isinstance(reponse_json['result'], dict)
        assert response.json() == {"error": False,
                                    "result": {"tensor_list": [2,4,6,8]}}

    except AssertionError:
        print(response.status_code)
        print(response.json())
        raise
