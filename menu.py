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
            print("What you want to do? For Help Type /?")
            x = input(">>> ")
            x=x.lower()
            x=x.split()
            if 'fetch' in x or 'get' in x or 'gather' in x or 'view' in x or 'show' in x or 'display' in x:
                print("Enter Only Those Filters With Which You Want To Search The Password")
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
            elif ('save' in x or 'add' in x or 'create' in x) and ('password' in x or 'account' in x):
                domain = input("Enter Domain Name: ")
                username = input("Enter Username: ")
                password =  passwordRecognizerAndGenerator()
                notes = input("Enter Any Required Notes: ")
                addIntoVault(domain,username,password,UUID,notes,cipher)
            elif ('update' in x or 'change' in x or 'alter' in x or 'modify' in x) and 'password' in x and 'master' not in x:
                domain = input("Enter Domain Name")
                username = input("Enter User Name")
                password =  passwordRecognizerAndGenerator()
                updateVault(username,domain,password,cipher)
            elif ('delete' in x or 'remove' in x or 'erase' in x) and 'password' in x:
                print("Enter Only Those Filters With Which You Want To Search The Password")
                domain = input("Enter Domain Name: ")
                username = input("Enter Username: ")
                notes = input("Enter Notes: ")
                if not domain:
                    domain=None
                if not username:
                    username=None
                if not notes:
                    notes=None
                deleteVault(UUID,cipher,domain,username,notes)
            elif 'report' in x or 'info' in x:
                vaultReport(UUID,cipher)
            elif ('change' in x or 'alter' in x or 'modify' in x or 'update' in x) and ('master password' in x or 'master' in x):
                x=input("Enter New Password!")
                updateMasterPassword(x,email,cipher,UUID)
                return
            elif ('delete' in x or 'remove' in x) and ('user' in x or 'account' in x):
                deleteUser(email,UUID)
                return
            elif 'help' in x or 'support' in x or '/?' in x:
                print("Try Using The Following Commands: ")
                print("""Create Password\nFetch Accounts\nChange Password\nDelete Password\nChange Master Password \nVault  Report\nDelete User""")
            elif 'logout' in x or 'signout' in x or 'exit' in x or 'close' in x:
                return
            else:
                print("Sorry! I could not understand. Pls Try Again")

            menu(UUID,cipher,email)