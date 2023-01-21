#!/bin/bash

#Comando para correr un contenedor en modo detach basado en la imagen que creamos anteriormente 'api_tenpo'
#Se expone el puerto 80 del contenedor al 80 local

docker run  -d -p 80:80 api_tenpo 