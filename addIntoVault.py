from cryptography.hazmat.primitives.kdf.pbkdf2  import PBKDF2HMAC
from cryptography.fernet import Fernet
from sqlalchemy import text,create_engine
from dotenv import get_key
import datetime
import base64
from time import sleep
from os import system,name
engine = create_engine(get_key('./.env',"USERS_connection_string"))
connection = engine.connect()
"""
Add into vault function adds a password to the user's vault after encrypting it thourougly using cipher object generated using user's master password and salt

"""

def addIntoVault(domain,username,password:str,uuid,notes,cipher):
    try:
        query = text('select * from vault where domain_name=:domain and username=:username and vault_uuid=:uuid')
        cur = connection.execute(query,{
            "domain":domain,
            "username":username,
            "uuid":uuid
        }).fetchall()
        if not cur:
            encrypted_password = cipher.encrypt(password.encode())
            query =  text(f'INSERT INTO vault values(:uuid,:username,:password,:notes,:date,:domain_name);')
            cur = connection.execute(query,{
                "uuid":uuid,
                "domain_name":domain,
                "username":username,
                "password":encrypted_password,
                "notes":notes,
                "date":datetime.datetime.utcnow()
            })
            connection.commit()
            print("Account Added Succesfully!")
            sleep(5)
            system('cls' if name=='nt' else 'clear')
        else:
            print("USER ALREADY EXISTS!")
            sleep(5)
            system('cls' if name=='nt' else 'clear')
    except Exception as e:
        print(e)