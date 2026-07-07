from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from os import urandom
from dotenv import get_key
from cryptography.fernet import Fernet,InvalidToken
from passwordRecognizerAndGenerator import PasswordGenerator
from sqlalchemy import text,create_engine
import uuid
import json
from login import login
import winreg as reg
from cryptography.hazmat.primitives.hashes import SHA256
import base64
from os import listdir,makedirs
def export(UUID,cipher:Fernet):
    connection = create_engine(get_key('./.env','USERS_connection_string')).connect()
    query =  text(f'select * from vault where vault_uuid = :uuid')
    cur = connection.execute(query,{
        "uuid":UUID
    }).fetchall()
    domain = []
    username=[]
    notes=[]
    passwords=[]
    date_created=[]
    salt = urandom(16)
    new_password = PasswordGenerator()
    key = PBKDF2HMAC(SHA256(),32,salt,1000000)
    key = key.derive(bytes(new_password.encode()))
    key = base64.urlsafe_b64encode(key)
    cipher2 = Fernet(key)
    for row in cur:
        username.append(row[1])
        domain.append(row[-1])
        notes.append(row[-3])
        date_created.append(row[-2])
        password = cipher.decrypt(bytes(row[2])).decode()
        encrypted_password = cipher2.encrypt(password.encode())
        passwords.append(encrypted_password.decode())
    data = {
    "VERSION":1,
    "UUID":UUID,
    "salt":base64.b64encode(salt).decode(),
    "domain":domain,
    "usernames":username,
    "notes":notes,
    "date_created":date_created,
    "passwords":passwords,
    }
    export_name = str(uuid.uuid4())
    f = open('Exports/{0}.txt'.format(export_name),'w')
    f.write(json.dumps(data))
    f.close()
    connection.close()
def importPasswords():
    makedirs("Exports",exist_ok=True)
    x = listdir('Exports/')
    if len(x):
        x=x[0]
    else:
        print("Paste you exported file in Exports Folder To Import It")
        return 
    d=open('Exports/{0}'.format(x))
    data = json.load(d)
    d.close()
    if data["VERSION"]==1:
        connection = create_engine(get_key('./.env','USERS_connection_string')).connect()
        password = input("Enter The Password Which You Were Given While Exporting: ")
        key = PBKDF2HMAC(SHA256(),32,base64.b64decode(data["salt"]),1000000)
        key = key.derive(password.encode())
        key = base64.urlsafe_b64encode(key)
        cipher = Fernet(key)
        try:
            for i in range(len(data['passwords'])):
                # Check This Line
                data['passwords'][i]=cipher.decrypt(bytes(data['passwords'][i].encode())).decode()
        except InvalidToken as e:
            print("Password Is Wrong!")
            return
        except  Exception as e:
            print("Something went Wrong!",e)
            return 
        print("FIRST VERIFY YOUR ACCOUNT CREDENTIALS TO PROCEED")
        password = input("Enter Your Master Password")
        software = reg.OpenKeyEx(reg.HKEY_CURRENT_USER,'SOFTWARE\\Password Manager')
        email = reg.QueryValueEx(software,"Email")[0]
        UUID = reg.QueryValueEx(software,"__VAULT_UUID__")[0]
        reg.CloseKey(software)
        query = text('select password,salt from '+email+';')
        response = connection.execute(query).fetchone()
        res = login(password,response[0])
        kdf = PBKDF2HMAC(SHA256(),32,bytes(response[1]),1000000)
        key = kdf.derive(bytes(password.encode()))
        key = base64.urlsafe_b64encode(key)
        cipher2 = Fernet(key)
        decision = input("Enter Merge to Add Those Accounts which are missing.\nEnter Override to alter the overlapping password accounts and add the missing ones")
        if  decision.lower() not in ['merge','override']:
            print("Invalid Input, retruning to main menu")
            return
        query = text('select * from vault where vault_uuid=:uuid and domain_name=:domain and username=:username')
        for i in range(len(data['passwords'])):
            cur = connection.execute(query,{
                'uuid':UUID,
                'domain':data['domain'][i],
                'username':data['usernames'][i],
            }).fetchall()
            if not len(cur):
                query = text('insert into vault values(:uuid,:username,:password,:notes,:date,:domain);')
                connection.execute(query,{
                    "uuid":UUID,
                    'domain':data['domain'][i],
                    'username':data['usernames'][i],
                    'password':cipher2.encrypt(bytes(data['passwords'][i].encode())),
                    'notes':data['notes'][i],
                    'date':data['date_created'][i],
                })
            elif decision.lower()=='override' and len(cur):
                query = text('update vault set password = :password where vault_uuid=:uuid and domain_name=:domain and username=:username;')
                connection.execute(query,{
                    "uuid":UUID,
                    'domain':data['domain'][i],
                    'username':data['usernames'][i],
                    'date':data['date_created'][i],
                    'password':cipher2.encrypt(bytes(data['passwords'][i].encode())),
                })
        connection.commit()
        connection.close()
    else:
        print("Sorry The Version Of This Export Isn't Supported")
importPasswords()