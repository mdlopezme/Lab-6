#!/usr/bin/env python3
from time import time, sleep

def secure(user_credentials, timeOut, end_threads):
    while(not end_threads[0]):
        if time() > (user_credentials[2]+timeOut):
            user_credentials[3] = False # Lock everything
        sleep(1)