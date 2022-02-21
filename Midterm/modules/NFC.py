#!/usr/bin/env python3
from time import time, sleep
from mfrc522 import SimpleMFRC522
import modules.ENVIRONMENT as ENVIRONMENT

def readNFC(user_credentials, kill_threads):
    # Setup NFC Reader
    reader = SimpleMFRC522()
    while(not kill_threads[0]):
        print("Waiting for authentication")
        
        id, user = reader.read(kill_threads)

        # print(id)
        # print(ENVIRONMENT.OLIVIER_ROGERS)
        # print(ENVIRONMENT.MOISES_LOPEZ)

        if str(id) == ENVIRONMENT.OLIVIER_ROGERS or str(id) == ENVIRONMENT.MOISES_LOPEZ:
            user_credentials[0] = id
            user_name = user.strip()
            if ""==user_name:
                user_name="John Doe"
            user_credentials[1] = user_name
            user_credentials[2] = time() 
            user_credentials[3] = True # Autheticated
            user_credentials[4] = False # Logged to database
            # print(f'Authenticated, found: {user}')
        else:
            user_credentials[0] = id
            user_credentials[1] = 'Unknown User'
            user_credentials[2] = time() 
            user_credentials[3] = False
            user_credentials[4] = False

        for _ in range(0,10):
            if kill_threads[0]:
                break
            sleep(.5)