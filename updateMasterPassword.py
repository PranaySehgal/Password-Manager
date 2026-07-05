from sqlalchemy import text,create_engine
from dotenv import get_key
from argon2 import PasswordHasher
import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.fernet import Fernet
"""
Update Master Password decrypts all the password with previous master password and encrypts them again with a new salt and new master password
Later These are stored back into the vault and masterPassword and salt are updated in the database
"""

def updateMasterPassword(password,email,cipher:Fernet,uuid):
    try:
        query = text('SELECT * FROM VAULT where VAULT_UUID=:uuid')
        connection = create_engine(get_key('./.env','USERS_connection_string')).connect()
        cur = connection.execute(query,{
            "uuid":uuid
        })
        cur= cur.fetchall()
        l=[]
        for row in cur:
            l.append([row[-1],row[1],bytes(row[2])])
        for i in l:
            i[-1]=cipher.decrypt(i[-1]).decode()
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(SHA256(),32,salt,1000000)
        key = kdf.derive(bytes(password.encode()))
        key = base64.urlsafe_b64encode(key)
        cipher2 = Fernet(key)
        for i in l:
            i[-1]=cipher2.encrypt(i[-1].encode())
        query = text('UPDATE VAULT SET PASSWORD=:password where vault_uuid=:uuid and username=:username and domain_name=:domain')
        for i in l:
            connection.execute(query,{
                "uuid":uuid,
                "username":i[1],
                "domain":i[0],
                "password":i[2],
            })
            connection.commit()
        connection.close()
        connection = create_engine(get_key('./.env','USERS_connection_string')).connect()
        query = text('UPDATE "{0}" set password=:password, salt=:salt'.format(email))
        ph = PasswordHasher()
        encrypted_password = ph.hash(password.encode())
        cur = connection.execute(query,{
            "password":encrypted_password,
            "salt":salt,
        })
        connection.commit()
        connection.close()
        print("MASTER PASSWORD UPDATED, Logging You Out IMMEDIATLEY!")
        
    except Exception as e:
        print(e)
    