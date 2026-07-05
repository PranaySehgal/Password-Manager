from cryptography.fernet import Fernet
from sqlalchemy import text,create_engine
from dotenv import get_key
from time import sleep
from os import system,name
def deleteVault(UUID,x,cipher:Fernet,username=""):
    engine = create_engine(get_key('./.env',"USERS_connection_string"))
    """
    DELETE Vault Deletes one/all ppasswords as per user's request using sqlachmy module
    """
    
    try:
        connection = engine.connect()
        if x=='ALL':
            query = text("DELETE FROM VAULT WHERE VAULT_UUID=:uuid")
            cur = connection.execute(query,{
                "uuid":UUID
            })
        else:
            query = text("DELETE FROM VAULT WHERE VAULT_UUID=:uuid and username=:username and domain_name=:domain")
            cur = connection.execute(query,{
                "uuid":UUID,
                "username":username,
                "domain":x
            })
        connection.commit()
        print("PASSWORD(s) DELETED SUCCESSFULLY!")
        sleep(5)
        system('cls' if name=='nt' else 'clear')
    except Exception as e:
        print(e)
    