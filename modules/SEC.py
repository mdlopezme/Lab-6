from time import time, sleep

def secure(user_credentials, timeOut):
    while(True):
        if time() > (user_credentials[2]+timeOut):
            user_credentials[3] = False # Lock everything
        sleep(1)