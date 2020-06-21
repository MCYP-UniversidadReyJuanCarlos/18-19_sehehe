# Descripción

Herramienta para borrar datos exif de las imagenes, cifrar las imágenes una por una y subirlas por separado a Google Drive.

# Características

Realiza un recorrido por el directorio que se le indique, en el irá borrando los datos EXIF, cifrando las imagenes, una por una usando SHA256 y la contraseña introducida. Después se subiran todas las imagenes cifradas por separado a Google Drive.

pip install -r requirements.txt
pip3 install -r requirements.txt

# Uso
sudo python3 encrypt.py
