#!/bin/bash
cd ./app

gunicorn -w ${WORKERS:=2} \
  -b 127.0.0.1:8080 -t ${TIMEOUT:=300} \
  -k uvicorn.workers.UvicornWorker \
  --log-config log.ini \
  --reload \
  main:app