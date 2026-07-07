import hashlib
import dotenv
import time
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import cryptography.hazmat.primitives.hashes as hashes
attempts=0
"""
Login function checks if the user has enetred correct credentials r not. if not, user is given 5 attempts and then a final attempt
After 2nd attempt, a sleep timer is initiated to prevent brute force attacks and fter last attempt the application closes
"""

def login(password,hash):
    global attempts
    ph = PasswordHasher()
    try:
        ph.verify(hash,password)
        attempts=0
        return True
    except:
        attempts+=1
        if attempts==3:
            print("Sorry, Due to repetitive password attempts, you have been locked out of the profile for 30 seconds: \n Attempts Remaining: 3")
            time.sleep(30)
        elif attempts==4:
            print("Sorry, Due to repetitive password attempts, you have been locked out of the profile for 60 seconds: \n Attempts Remaining: 2")
            time.sleep(60)
        elif attempts==5:
            print("Sorry, Due to repetitive password attempts, you have been locked out of the profile for 300 seconds: \n Attempts Remaining: 1")
            time.sleep(300)
        elif attempts==6:
            print("Sorry, Due to repetitive password attempts, you have been locked out of the profile. \n Attempts Remaining: 0")
            print("Closing The Application.............")
            return "CLOSE"
        return False
