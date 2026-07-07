import os
import winreg as reg
from cryptography.hazmat.primitives.kdf.pbkdf2  import PBKDF2HMAC
import cryptography.hazmat.primitives.hashes
import uuid
import dotenv
import hashlib
from createNewVault import *
from login import *
from accessVault import *
from menu import *
import re
import base64
from cryptography.fernet import Fernet
from passwordRecognizerAndGenerator import *
val=None
def createVaultUUID():
    return str(uuid.uuid4())+str(uuid.uuid7())
VAULT_UUID = None
"""
The Main Starting Point of The application, it initiates the database connection, validates if the user has already uses this app on this device
It gathers authentication info from the user.
If he is authenticated he autorizes the user and sends him to the Menu File
Windows Registry saves the Vault Unique Identifier and Email ID so the user does not have to enter the credentials over and over again to login

"""

def init():
    print("WELCOME TO PASSWORD VAULT AKA PASSWORD MANAGAER Version 1.0")
    path = reg.HKEY_CURRENT_USER
    try:
        software = reg.OpenKeyEx(path,'SOFTWARE\\Password Manager')
        val = reg.QueryValueEx(software,"__VAULT_UUID__")[0]
        email = reg.QueryValueEx(software,"Email")[0]
        password = input("Enter A Password!: ")
        response=createNewVault(email,None,None)
        res = login(password,response[1])
        
    except Exception as e:
        print(e)
        software = reg.OpenKeyEx(path,'SOFTWARE\\')
        email = input("Enter Your Email ID: ")
        condition = '[a-z 0-9]+[\\ ._ ]?[a-z 0-9]+[@]\\w+[.]\\w{2,3}$'
        
        if not re.search(condition,email):
            print("INVALID EMAIL")
            return init()
        password = passwordRecognizerAndGenerator()
        newKey =  reg.CreateKey(software,"Password Manager")
        val= createVaultUUID()
        reg.SetValueEx(newKey,'__VAULT_UUID__',0,reg.REG_SZ,val)
        reg.SetValueEx(newKey,'Email',0,reg.REG_SZ,email)
        if newKey:
            reg.CloseKey(newKey)
        
        response = createNewVault(email,val,password)
        res = login(password,response[1])
    kdf = PBKDF2HMAC(hashes.SHA256(),32,bytes(response[2]),1000000)
    key = kdf.derive(bytes(password.encode()))
    key = base64.urlsafe_b64encode(key)
    cipher = Fernet(key)
    if res=="CLOSE":
        return
    if not res:
        print("Wrong Username Or Password Detected. Kindly Try Again")
        init()
    VAULT_UUID = val
    del val
    menu(VAULT_UUID,cipher,email)
init()
0