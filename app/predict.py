#!/usr/bin/python3
# -*- coding: utf-8 -*-

import torch


def predict(input: torch.Tensor) -> torch.Tensor:
    """
    Realiza la preciccion multiplicando el tensor por 2

    """

    #En caso de llamar al modelo pasar el package como parametro de la funcion e invocarlo
    #model = package['model']
    #result = model(input)

    result = torch.mul(input, 2)

    return result