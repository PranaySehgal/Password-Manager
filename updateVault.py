from sqlalchemy import text,create_engine
from cryptography.fernet import Fernet
from time import sleep
from os import system,name
from dotenv import get_key
def updateVault(username,domain,password,cipher:Fernet):
    """
    Update Vault uppdates the password of the selected password to a new one by changing the previous encrypted password with a new one
    
    """
    
    engine = create_engine(get_key('./.env','USERS_connection_string'))
    connection = engine.connect()
    try:
        password = cipher.encrypt(password.encode())
        query=text("UPDATE VAULT SET PASSWORD = :password where username = :username and  domain_name=:domain;")
        cur = connection.execute(query,{
            "password":password,
            "domain":domain,
            "username":username
        })
        connection.commit()
        print("UPDATION WAS SUCCESSFUL")
        sleep(5)
        system('cls' if name=='nt' else 'clear')
    except Exception as e:
        print("Some Error Occured!",e)
        return "ERROR"
    