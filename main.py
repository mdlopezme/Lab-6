#!/usr/bin/env python3
import modules.NFC as NFC
import modules.LCD as LCD
import modules.BELL as BELL
import modules.SERVO as SERVO
import modules.LOGGER as LOGGER
import modules.SEC as SEC
import modules.WEBSERVER as WEBSERVER

from time import time, sleep
import threading
 # This is intentional

def main():
    print('Starting Program')

    TIMEOUT = 5
    user_credentials = [0, '', time()-TIMEOUT, False, True ]
    bell_has_been_logged =[ True ]
    kill_threads = [False]

    web_server=WEBSERVER.WebLock()

    try:
        NFC_reader = threading.Thread(target=NFC.readNFC, args=(user_credentials, kill_threads), name="Authentication")
        display = threading.Thread(target=LCD.update, args=(user_credentials, kill_threads), name="Display")
        security = threading.Thread(target=SEC.secure, args=(user_credentials,TIMEOUT, kill_threads), name="Security")
        bell = threading.Thread(target=BELL.ringer, args=(bell_has_been_logged, kill_threads), name="Bell")
        servo = threading.Thread(target=SERVO.servo, args=(user_credentials, kill_threads), name="Servo Motor")
        logger = threading.Thread(target=LOGGER.log, args=(user_credentials, bell_has_been_logged, kill_threads), name="Logging")
        
        print('Starting threads')
        web_server.start()
        NFC_reader.start()
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
        while NFC_reader.is_alive() or display.is_alive() or security.is_alive() or bell.is_alive() or servo.is_alive() or logger.is_alive():
            sleep(1)

        print('Finally Exiting')

if __name__ == '__main__':
    main()