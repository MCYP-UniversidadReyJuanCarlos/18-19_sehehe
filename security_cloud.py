import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import fnmatch
import piexif
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import getpass



ruta_app = input("Ruta a sincronizar: ")

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


def Main():
	filename = []
	choice = input("Quieres (S)incronizar o (D)escifrar?: ")
	if choice == 'S' or choice == 's':
		password = getpass.getpass("Contraseña para cifrar: ")
		for root, direct, files in os.walk(ruta_app, topdown=True):
			for file in files:
				if file.lower().endswith(".jpeg") or file.lower().endswith(".jpg"):
					Ejecutar(os.path.join(root, file))
					filename = file
					ruta = os.path.join(root)
					os.chdir(ruta)
					encrypt(getKey(password), filename)
					os.remove(filename)
					print("Fichero cifrado: {}".format(file))
				else:
					filename = file
					ruta = os.path.join(root)
					os.chdir(ruta)
					encrypt(getKey(password), filename)
					os.remove(filename)
					print("Fichero cifrado: {}".format(file))
		for root, direct, files in os.walk(ruta_app, topdown=True):
			for file in files:
				if fnmatch.fnmatch(file,'(cifrado)*'):
					ruta = os.path.join(root)
					os.chdir(ruta)
					with open(file,"r") as f:
						fn = os.path.basename(f.name)
						file_drive = drive.CreateFile()
						file_drive.SetContentFile(file)
						file_drive.Upload()
						file_drive.content.close()
					os.remove(file)
					print ("El fichero: " + fn + " fue subido")
	elif choice == 'D' or choice == 'd':
		password = getpass.getpass("Contraseña para descifrar: ")
		for root, direct, files in os.walk(ruta_app, topdown=True):
			for file in files:
				if fnmatch.fnmatch(file,'(cifrado)*'):
					filename = file
					ruta = os.path.join(root)
					os.chdir(ruta)
					decrypt(getKey(password), filename)
					os.remove(filename)
					print("Fichero descifrado: {}".format(file))
	else:
		print("No se ha seleccionado ninguna opción, cerrando...")

def Ejecutar(file):
    print("Eliminando datos exif {}".format(file))
    piexif.remove(file)


def encrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = "(cifrado)" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = filename[9:]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()



if __name__ == '__main__':
    Main()

