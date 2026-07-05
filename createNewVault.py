from sqlalchemy import text,create_engine
import dotenv
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import hashlib
def createPassHash(originalPassword:str):
    ph = PasswordHasher()
    password =  ph.hash(originalPassword)
    return password
"""
CreateNewVault creates a vault for new user if he does not exist else returns the already stored info
"""

    
def createNewVault(email:str,uuid:str|None,password:str|None):
    engine = create_engine(dotenv.get_key('./.env',"USERS_connection_string"))
    connection =  engine.connect()
    try:
        cur = connection.execute(text("select count(table_name) from information_schema.tables where table_name = '{0}'".format(email)))
        if not cur.fetchall()[0][0]:
            pass
            raise Exception("NEW USER CREATION")
        else:
            cur = connection.execute(text('select vault_uuid, password, salt from "{0}"'.format(email)))
            res=cur.fetchone()
            return tuple(res)
    except Exception as e:
        salt = os.urandom(16)
        password=createPassHash(password)
        cur = connection.execute(text('CREATE TABLE "{0}" (Vault_UUID varchar(900), PASSWORD VARCHAR(900), Salt BYTEA);'.format(email)))
        connection.commit()
        query = text(f'''
        INSERT INTO "{email}"
        (vault_uuid, password, salt)
        VALUES (:vault_uuid, :password, :salt)
        ''')

        connection.execute(
            query,
            {
                "vault_uuid": uuid,
                "password": password,
                "salt": salt
            }
        )

        connection.commit()
        connection.close()
        print("NEW PROFILE CREATED SUCCESFULLY")
        return (uuid,password,salt)

        