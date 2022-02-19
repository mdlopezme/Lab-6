#!/usr/bin/env python3
import modules.NFC as NFC
import modules.LCD as LCD
import modules.BELL as BELL
import modules.SERVO as SERVO
import modules.LOGGER as LOGGER
import modules.WEBSERVER as WEBSERVER
import modules.SEC as SEC

import os

from time import time, sleep
import threading
import RPi.GPIO as GPIO

def main():
    print('Starting Program')

    [lcd, reader] = LCD.setUp()
    TIMEOUT = 5
    user_credentials = [0, '', time()-TIMEOUT, False, True ]
    ringer_info =[ False, time()-TIMEOUT, True ]
    kill_threads = [False]

    try:
        authentication = threading.Thread(target=NFC.readNFC, args=(reader,user_credentials, TIMEOUT, kill_threads))
        display = threading.Thread(target=LCD.update, args=(lcd, user_credentials, kill_threads))
        security = threading.Thread(target=SEC.secure, args=(user_credentials,TIMEOUT, kill_threads))
        bell = threading.Thread(target=BELL.ringer, args=(ringer_info, kill_threads))
        servo = threading.Thread(target=SERVO.act, args=(user_credentials, TIMEOUT, kill_threads))
        logger = threading.Thread(target=LOGGER.log, args=(user_credentials, ringer_info, kill_threads))
        web_server = threading.Thread(target=WEBSERVER.main, args=(kill_threads,))

        authentication.start()
        display.start()
        security.start()
        bell.start()
        servo.start()
        logger.start()
        web_server.start()

        while True:
            sleep(100)

    except KeyboardInterrupt:
        kill_threads[0] = True
        while authentication.is_alive() or display.is_alive() or security.is_alive() or bell.is_alive() or servo.is_alive() or logger.is_alive():
            print( (authentication.is_alive(),display.is_alive(),security.is_alive(), bell.is_alive(),servo.is_alive(),logger.is_alive()))
            sleep(1)
    finally:
        print('Finally Exitinng')
        os._exit(os.EX_OK)

if __name__ == '__main__':
    main()