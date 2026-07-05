from sqlalchemy import text,create_engine
from dotenv import get_key
from cryptography.fernet import Fernet
"""
This Duplicate Detection is Used to detect and return domains that have used duplicate passwords
"""

def dupllicateDetection(UUID,cipher:Fernet):
    d={}
    connection = create_engine(get_key('./.env','USERS_connection_string')).connect()
    query = text("SELECT  * FROM VAULT WHERE VAULT_UUID=:uuid")
    cur = connection.execute(query,{
        "uuid":UUID
    }).fetchall()
    for i in cur:
        password=cipher.decrypt(bytes(i[2])).decode()
        if d.get(password,-90)==-90:
            d[password]=[i[1]]
        else:
            d[password].append(i[1])
    l=[]
    count=0
    for i in d:
        if len(d[i])==1:
            pass
        else:
            count+=1
            for j in range(len(d[i])):
                if j==0:
                    continue
                else:
                    l.append(d[i][j])
    return l
    
    