from random import randint
import pyperclip
from time import sleep
def passwordRecognizerAndGenerator():
    """
    Password recognizer and generator identifies if the given password is secure or not. if not the user is asked to change the password.
    Weak or insecure passwords are not allowed in this app.
    Also if the user wants  he can get an auto-generated password that fulfills all the conditions
    
    """
    
    print("PASSWORD INSTRUCTIONS: Length: 16-20, Upper Case,Lower Case, Symbols({}[]-+=;:.,/|*&^%$#@!() and Numbers")
    password = input("Enter A Password Or Leave It Empty To Auto-Generate One")
    chars = 'abcdefghijklmnopqrstuvwxyz'
    uppers = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    symbols='{}[]-+=;:.,/|*&^%$#@!()'
    nums='1234567890'
    if not password:
        length = randint(16,20)
        options = [chars,uppers,symbols,nums]
        s=''
        length-=4
        # Length has been decreased by 4 as each type of  character will be added to random password before randomizing them as it might happen that a particular catagory might not get 
        # even one chance as its random
        s+=chars[randint(0,len(chars)-1)]
        s+=nums[randint(0,len(nums)-1)]
        s+=uppers[randint(0,len(uppers)-1)]
        s+=symbols[randint(0,len(symbols)-1)]
        while length:
            option = options[randint(0,3)]
            s+=option[randint(0,len(option)-1)]
            length-=1
        print("Password Has Been Copied to your clipboard. After 60 seconds it will be wiped. Kindly save it somewhere safe or best learn it")
        pyperclip.copy(s)
        sleep(60)
        if pyperclip.paste()==s:
            pyperclip.copy(" ")
        return s
    else:
        if len(password)<16:
            print("Too Small Password!")
            return passwordRecognizerAndGenerator()
        upper = False
        num = False
        symbol = False
        char=False
        for i in password:
            if i in uppers:
                upper=True
            elif i in nums:
                num = True
            elif i in symbols:
                symbol=True
            elif i in chars:
                char=True
            else:
                print('(',i,") This Is not a allowed character in a password")
                return passwordRecognizerAndGenerator()
        if not char and upper and num and symbol:
            print("The Pattern Is Not Matched: 1 Upper, 1 Lower, 1 Nums, 1 Lower")
            return passwordRecognizerAndGenerator()
        else:
            return password


