#!/usr/bin/python3
# -*- coding: utf-8 -*-

import torch


def predict(package: dict, input: torch.Tensor) -> torch.Tensor:
    """
    Realiza la preciccion multiplicando el tensor por 2

    """

    model = package['model']

    result = model(input)

    return result