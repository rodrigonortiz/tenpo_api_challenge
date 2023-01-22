# Challenge Tenpo ML Engineer | Rodrigo Ortiz


He creado una API con FastAPI para servir el modelo proporcionado en el challenge (No es un modelo en realidad, si no una operacion de multiplicacion de un tensor por un escalar (2) que oficia de inferencia para coincidir con lo requerido, de todas formas el codigo esta adaptado para cargar el modelo que desees. La API recibe como input una lista de valores numericos, convierte esa lista en un tensor, hace la multiplicacion sobre el mismo, convierte el tensor resultado en lista y lo devuelve.
Ademas cuenta con un pipeline de CI/CD de GitHub Actions, aprovisionamiento de recursos con Terraform y despliegue en GCP.

Esta lista para que hagas un build con el `Dockerfile` la puedas correr y probar en tu maquina local siguiendo estos pasos:

Ejecutar primero `docker_build.sh` y cuando finalice, podes crear un contenedor basado en la imagen recien creada con `docker_run.sh`

La request body que recibe tiene el siguiente formato:

```
{
  "values_list": [
    1,2,3,4,5
  ]
}
```

Y el body result:
```
{
  "error": false,
  "result": {
    "tensor_list": [
      2,
      4,
      6,
      8,
      10
    ]
  }
}
```

Los directorios se encuentran de la siguiente forma:

```
.
└── TENPO API CHALLENGE/
    ├── .github/
    │   └── workflows/
    │       └── workflow.yaml
    ├── app/
    │   ├── log
    │   ├── tests/
    │   │   ├── __init__.py
    │   │   └── test_api.py
    │   ├── __init__.py
    │   ├── config.py
    │   ├── exception_handler.py
    │   ├── log.ini
    │   ├── main.py
    │   ├── predict.py
    │   ├── schema.py
    │   └── test.sh
    ├── model
    ├── terraform/
    │   └── main.tf
    ├── venv
    ├── docker_build.sh
    ├── docker_run.sh
    ├── Dockerfile
    ├── Readme.md
    ├── requirements.txt
    └── start.sh
```


En la carpeta `app` se encuentran todos los scripts necesarios para el funcionamiento de la API, el principal y donde se encuentra el endpoint es `main.py`, tambien le he agregado un directorio donde se guardan los logs (la configuracion se realiza en `logs.ini`), un archivo `config.py` donde se definen las configuraciones del proyecto, un script `schema.py` que contiene los schemas de inputs y outputs necesarios para usar con la libreria pydantic, un script `predict.py` donde se encuentra la definicion de la funcion de prediccion que se llama cada vez que le hacemos un request a la API, tambien he agregado para manejo de errores (excepciones) personalizadas en `exception_handler.py` tanto para errores genericos o en la request y un folder llamado test donde se encuentra un test de respuesta de la prediccion (si desea correrlo ejecute el script bash `test.sh`).


En el directorio `Model` puede cargar su modelo si lo deseea (Reminder: estoy emulando el modelo con una simple operacion de tensores, pero el codigo se adapta facilmente a un modelo cargado que haga esto mismo, vea las lineas comentadas que hay en `main.py`.

En `.github/workflows` se encuentra el `workflow.yaml` con las definiciones necesarias para generar el CI/CD (Reemplazar `ID_PROYECTO_GCP` por su id real de proyencto en `GCP` y no se olvide de cargar en las secrets de GitHub la variable `GCLOUD_SERVICE_KEY` con la key proporcionada.

En `terraform/main.tf` va a encontrar las definiciones necesarias para montar la infraestructura en `GCP` (Cloud Run API).

Con solo hacer un push a la rama `main` del repositorio ya deberia ver en el apartado `Actions` el pipeline de CI/CD ejecutandose.


