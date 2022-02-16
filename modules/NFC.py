from time import time, sleep

def readNFC(reader,user_credentials, timeOut):
    while(True):
        print("Waiting for authentication")
        id, user = reader.read()

        # print(id)

        if id == 397475334654 or id == 288461690070:
            user_credentials[0] = id
            user_credentials[1] = user
            user_credentials[2] = time() 
            user_credentials[3] = True
            user_credentials[4] = False
            # print(f'Autheticated, found: {user}')
        else:
            user_credentials[0] = id
            user_credentials[1] = 'Unknown User'
            user_credentials[2] = time() 
            user_credentials[3] = False
            user_credentials[4] = False

        sleep(timeOut)