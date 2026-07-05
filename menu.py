from accessVault  import accessVault
from accessVault import *
from addIntoVault import *
from updateVault import *
from deleteVault import deleteVault
from vaultReport import vaultReport
from updateMasterPassword import *
from os import system
from time import sleep
from deleteUser import *
from passwordRecognizerAndGenerator import *
"""
This is the function that runs all the other functions as per user requests

"""
def menu(UUID,cipher,email):
        print("Great!. Now You Are Finally Logged In.")
        print('1. Fetch All Passwords')
        print('2. Add A New Password')
        print('3. Update A Singular Password')
        print('4. Delete A Password')
        print('5. Delete All Passwords(BE CAREFUL THIS IS IRREVERSIBLE)!')
        print('6. Vault Report')
        print('7. Change Master Password')
        print('8. Delete Account')
        print('9. Logout')
        x = input("Enter The Desired Option")
        if not x.isdigit():
            print("INVALID OPTION SELECTED")
            print('Returning Back To Menu!')
            menu(UUID,cipher,email)

        else:
            x = int(x)
            if x==1:
                print("Enter Only Those values with what you want to search")
                domain = input("Enter Domain Name: ")
                username = input("Enter Username: ")
                notes = input("Enter Notes: ")
                if not domain:
                    domain=None
                if not username:
                    username=None
                if not notes:
                    notes=None
                accessVault(UUID,cipher,domain,username,notes)

            elif x==2:
                domain = input("Enter Domain Name: ")
                username = input("Enter Username: ")
                password =  passwordRecognizerAndGenerator()
                notes = input("Enter Any Required Notes: ")
                addIntoVault(domain,username,password,UUID,notes,cipher)
            elif x==3:
                domain = input("Enter Domain Name")
                username = input("Enter User Name")
                password =  passwordRecognizerAndGenerator()
                updateVault(username,domain,password,cipher)
            elif x==4:
                x=input("Enter The Domain Name You Want To Delete")
                username=input("Enter The Username You Want To Delete")
                deleteVault(UUID,x,cipher,username)
            elif x==5:
                deleteVault(UUID,"ALL",cipher)
            elif x==6:
                vaultReport(UUID,cipher)
            elif x==7:
                x=input("Enter New Password!")
                updateMasterPassword(x,email,cipher,UUID)
                return
            elif x==8:
                deleteUser(email,UUID)
                return
            else:
                return

            menu(UUID,cipher,email)