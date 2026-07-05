from sqlalchemy import create_engine,text
from dotenv import get_key
import winreg as reg
"""
This Function Deletes User and All Linked Passwords from the account
"""

def deleteUser(email,UUID):
    connection = create_engine(get_key("./.env",'USERS_connection_string')).connect()
    query1= text('delete from vault where vault_uuid=:uuid')
    connection.execute(query1,{
        "uuid":UUID
    })
    query1 = text('drop table "{0}"'.format(email))
    connection.execute(query1)
    connection.commit()
    connection.close()
    path = reg.HKEY_CURRENT_USER
    reg.DeleteKey(path,"SOFTWARE\\Password Manager")
    print("User Deleted Succesfully!")