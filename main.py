#!/usr/bin/env python3
import modules.NFC as NFC
import modules.LCD as LCD
import modules.BELL as BELL
import modules.SERVO as SERVO
import modules.LOGGER as LOGGER
# import modules.WEBSERVER as WEBSERVER
import modules.SEC as SEC
import modules.Webserver as Webserver

import os

from time import time, sleep
import threading
import RPi.GPIO as GPIO

def main():
    print('Starting Program')
    # GPIO.setmode(GPIO.BCM)
    [lcd, reader] = LCD.setUp()
    TIMEOUT = 5
    user_credentials = [0, '', time()-TIMEOUT, False, True ]
    ringer_info =[ False, time()-TIMEOUT, True ]
    kill_threads = [False]

    web_server=Webserver.WebLock()

    try:
        authentication = threading.Thread(target=NFC.readNFC, args=(reader,user_credentials, TIMEOUT, kill_threads), name="Authentication")
        display = threading.Thread(target=LCD.update, args=(lcd, user_credentials, kill_threads), name="Display")
        security = threading.Thread(target=SEC.secure, args=(user_credentials,TIMEOUT, kill_threads), name="Security")
        bell = threading.Thread(target=BELL.ringer, args=(ringer_info, kill_threads), name="Bell")
        servo = threading.Thread(target=SERVO.act, args=(user_credentials, TIMEOUT, kill_threads), name="Servo Motor")
        logger = threading.Thread(target=LOGGER.log, args=(user_credentials, ringer_info, kill_threads), name="Logging")
        # web_server = threading.Thread(target=WEBSERVER.main, args=(kill_threads,))
        # web_server = threading.Thread(target=web_server_obj.start, name="web server")
        
        print('Starting threads')
        web_server.start()
        authentication.start()
        display.start()
        security.start()
        bell.start()
        servo.start()
        logger.start()
        

        while True:
            sleep(100)

    except (Exception, KeyboardInterrupt) as e:
        print(e)
        
    finally:
        print('Please wait, killing threads')
        web_server.stop()
        kill_threads[0] = True
        while authentication.is_alive() or display.is_alive() or security.is_alive() or bell.is_alive() or servo.is_alive() or logger.is_alive():
            sleep(1)
            print('Workin...')
        # GPIO.setmode(GPIO.BCM)
        # GPIO.cleanup()
        print('Finally Exiting')

if __name__ == '__main__':
    main()