#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import torch


# Configuracion para todos los ambientes
GLOBAL_CONFIG = {
    "MODEL_PATH": "../model/model.pt"
}

# Configuracion especifica para cada ambiente, or overwrite of GLOBAL_CONFIG
ENV_CONFIG = {
    "development": {
        "DEBUG": True
    },

    "staging": {
        "DEBUG": True
    },

    "production": {
        "DEBUG": False
    }
}

def get_config() -> dict:
    """
    Configuracion para el ambiente actual
    

    return: Python dict
    """

    # detectar ambiente actual
    ENV = os.environ['PYTHON_ENV'] if 'PYTHON_ENV' in os.environ else 'development'
    ENV = ENV or 'development'

    # Raisear error si el ambiente no se encuentra en la configuracion de ENV_CONFIG
    if ENV not in ENV_CONFIG:
        raise EnvironmentError(f'Config for envirnoment {ENV} not found')

    # Actualiza la configuracion global sumando la del ambiente
    config = GLOBAL_CONFIG.copy()
    config.update(ENV_CONFIG[ENV])

    config['ENV'] = ENV

    # Verifica si cuda esta disponible, caso contrario usa CPU
    config['DEVICE'] = 'cuda' if torch.cuda.is_available() and config['USE_CUDE_IF_AVAILABLE'] else 'cpu'

    return config


# Carga config
CONFIG = get_config()