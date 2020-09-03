# Project title
DESARROLLO DE UNA HERRAMIENTA DE PRIVACIDAD PARA SISTEMAS DE ALMACENAMIENTO CLOUD

## Project description

Este trabajo se ha dedicado a automatizar el proceso de añadir una capa extra de seguridad en entornos de sistemas de almacenamiento en la nube. Gracias a ello, al utilizar la herramienta desarrollada en este trabajo se previene en gran medida un acceso a datos no autorizados si se llega a romper o saltar la seguridad de algunos de estos sistemas. También ayuda a añadir una capa de privacidad al eliminar todos los datos exif de las fotos, que contienen datos tan sensibles cómo la ubicación donde se realizó, fecha, hora, dispositivo con el que se realizó la foto, etc.

## Features

Realiza un recorrido por el directorio que se le indique, en el irá borrando los datos EXIF, cifrando las imagenes, una por una usando SHA256 y la contraseña introducida. Después se subiran todas las imagenes cifradas por separado a Google Drive.

> pip install -r requirements.txt

## How to run

> python3 security_cloud.py

> python3 security_cloud_graph.py
