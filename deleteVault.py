from cryptography.fernet import Fernet
from sqlalchemy import text,create_engine
from dotenv import get_key
from time import sleep
from os import system,name
def deleteVault(UUID,cipher:Fernet,domain,username,notes):
    engine = create_engine(get_key('./.env',"USERS_connection_string"))
    """
    DELETE Vault Deletes one/all ppasswords as per user's request using sqlachmy module
    """
    
    try:
        connection = engine.connect()
        d={
            "uuid":UUID,
        }
        query = f"DELETE FROM VAULT WHERE VAULT_UUID = :uuid"
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
        connection.commit()
        print("PASSWORD(s) DELETED SUCCESSFULLY!")
        sleep(5)
        system('cls' if name=='nt' else 'clear')
    except Exception as e:
        print(e)
    