from cryptography.hazmat.primitives.kdf.pbkdf2  import PBKDF2HMAC
from sqlalchemy import text,create_engine
from dotenv import get_key
import base64
import pyperclip
import tabulate
import time
from os import system, name
from time import sleep
from cryptography.fernet import Fernet
engine = create_engine(get_key('./.env',"USERS_connection_string"))
connection = engine.connect()
"""
Access Vault Function Allows the User to access the passwords that he has stored. he gives the user option to add filters to access a particular set of passwords
Passwords are fetched, they are decrypted using the cipher object sent by the parent function. After decryption it is converted to 
bytes and later decoded to convert into normal text
the passwords are copied into user's clipboard for a short duration and then over-written by a blank statement if he has not copied anything else

"""

def accessVault(UUID,cipher:Fernet,domain,username,notes):
    try:
        d={
            "uuid":UUID,
        }
        query = f"SELECT  * FROM VAULT WHERE VAULT_UUID = :uuid"
        if domain!=None:
            d["domain"]=domain
            query+=" and domain_name=:domain"
        if username!=None:
            d["username"]=username
            query+=" and username=:username"
        if notes!=None:
            query+=" and notes=:notes"
            d['notes']=notes
        query = text(query)
        cur = connection.execute(query,d)
        res = cur.fetchall()
        res = list(res)
        for i in range(len(res)):
            encrypted_pass = res[i][2]
            encrypted_pass = bytes(encrypted_pass)
            password = cipher.decrypt(bytes(encrypted_pass)).decode()
            res[i]=list(res[i])
            res[i][2]=password
            res[i].insert(0,i+1)
        list_data = [['Option Number','Domain Name','Username','Date-Time Created','Notes']]
        for i in res:
            list_data.append([i[0],i[-1],i[2],i[-2],i[-3]])
        print(tabulate.tabulate(list_data,headers='firstrow',tablefmt='fancy_grid'))
        x=(input("Enter A option for the given Passwords. The password will be automatically copied for you for 60 seconds after which it will be removed from the clipboard if nothing else is copied after copying passwords"))
        if not x.isdecimal():
            print("INVALID INPUT, LOADING MENU")
            sleep(3)
            system('cls' if name=='nt' else 'clear')
            return 
        elif int(x)>=len(list_data):
            print("INVALID INPUT, LOADING MENU")
            sleep(3)
            system('cls' if name=='nt' else 'clear')
            return 
        else:
            x=int(x)
            pyperclip.copy(res[x-1][3])
            time.sleep(60)
            if pyperclip.paste()==res[x-1][3]:
                pyperclip.copy(" ")
            print("Clipboard Cleared............")
            sleep(5)
            system('cls' if name=='nt' else 'clear')
        
            
        
    except Exception as e:
        print("Error Occured",e)