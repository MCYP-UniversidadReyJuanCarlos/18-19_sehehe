import wx
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import fnmatch
import piexif
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


class MiFrame(wx.Frame):
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)

        self.mainsz = wx.BoxSizer(wx.VERTICAL)
        self.inputsz = wx.FlexGridSizer(rows=2, cols=2, hgap=5, vgap=5)
        self.buttonsz = wx.BoxSizer(wx.HORIZONTAL)


        self.labelB = wx.StaticText(self, wx.ID_ANY, "Contraseña:")

        
        self.A = wx.DirDialog(self, "Selecciona la ruta a sincronizar", style=wx.DD_DEFAULT_STYLE)
        self.A.ShowModal()
        self.B = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)


        self.sync = wx.Button(self, label="Sincronizar")
        self.sync.Bind(wx.EVT_BUTTON, self.Primary)
        self.desc = wx.Button(self, label="Descifrar")
        self.desc.Bind(wx.EVT_BUTTON, self.Secondary)
        self.close = wx.Button(self, label="Cerrar")
        self.close.Bind(wx.EVT_BUTTON, self.onClose)


        for obj in [self.labelB, self.B]:
            self.inputsz.Add(obj, 1, wx.EXPAND|wx.ALL, 2)
        self.inputsz.AddGrowableCol(1)

        for obj in [self.sync, self.desc, self.close]:
            self.buttonsz.Add(obj, 5, wx.EXPAND|wx.ALL, 2)
            obj.SetInitialSize((20,-1))


        self.mainsz.Add(self.inputsz, 2, wx.EXPAND|wx.ALL, 5)
        self.mainsz.Add(self.buttonsz, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.mainsz)

        self.Centre(True)
        self.Show()

    def Primary(self, event):
        filename = []
        ruta_app = self.A.GetPath()
        password = self.B.GetValue()
        self.Close()

        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

        for root, direct, files in os.walk(ruta_app, topdown=True):
            for file in files:
                if (file.lower().endswith(".jpeg") or file.lower().endswith(".jpg")):
                    self.ejecutar(os.path.join(root, file))
                    filename = file
                    ruta = os.path.join(root)
                    os.chdir(ruta)
                    self.encrypt(self.getKey(password), filename)
                    os.remove(filename)
                    print("Fichero cifrado: {}".format(file))
                else:
                    filename = file
                    ruta = os.path.join(root)
                    os.chdir(ruta)
                    self.encrypt(self.getKey(password), filename)
                    os.remove(filename)
                    print("Fichero cifrado: {}".format(file))
        for root, direct, files in os.walk(ruta_app, topdown=True):
            for file in files:
                if fnmatch.fnmatch(file,'(cifrado)*'):
                    ruta = os.path.join(root)
                    os.chdir(ruta)
                    with open(file,"r") as f:
                        fn = os.path.basename(f.name)
                        file_drive = self.drive.CreateFile()
                        file_drive.SetContentFile(file)
                        file_drive.Upload()
                        file_drive.content.close()
                    os.remove(file)
                    print ("El fichero: " + fn + " fue subido.")

    def Secondary(self,event):
        filename = []
        ruta_app = self.A.GetPath()
        password = self.B.GetValue()
        self.Close()

        for root, direct, files in os.walk(ruta_app, topdown=True):
            for file in files:
                if fnmatch.fnmatch(file,'(cifrado)*'):
                    filename = file
                    ruta = os.path.join(root)
                    os.chdir(ruta)
                    self.decrypt(self.getKey(password), filename)
                    os.remove(filename)
                    print("Fichero descifrado: {}".format(file))

    def ejecutar(self, file):
        print("Eliminando datos exif {}".format(file))
        piexif.remove(file)


    def encrypt(self, key, filename):
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


    def getKey(self, password):
        hasher = SHA256.new(password.encode('utf-8'))
        return hasher.digest()

    def decrypt(self, key, filename):
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

    def onClose(self, event):
        self.Close()
            
if __name__=='__main__':
    app = wx.App() 
    fr = MiFrame(None, -1, "Privacidad y Seguridad - Google Drive", size=(600,110))
    app.MainLoop()



