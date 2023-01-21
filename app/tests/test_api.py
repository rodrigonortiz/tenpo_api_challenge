#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from ..main import app
import pytest


@pytest.fixture
def client():
    # use "with" statement to run "startup" event of FastAPI
    with TestClient(app) as c:
        yield c


def test_main_predict(client):
    """
    Test respuesta prediccion
    """

    headers = {}
    body = {
        [1,2,3,4]
    }

    response = client.post("/api/predict",
                           headers=headers,
                           json=body)

    try:
        assert response.status_code == 200
        reponse_json = response.json()
        assert reponse_json['error'] == False
        assert isinstance(reponse_json['results']['setosa'], float)
        assert isinstance(reponse_json['results']['pred'], str)

    except AssertionError:
        print(response.status_code)
        print(response.json())
        raise