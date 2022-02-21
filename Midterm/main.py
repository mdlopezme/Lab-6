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

def main():
    print('Starting Program')

    TIMEOUT = 5
    user_credentials = [0, '', time()-TIMEOUT, False, True ]
    record_bell_event =[ False ]
    end_threads = [False]

    web_server=WEBSERVER.WebLock()

    try:
        NFC_reader = threading.Thread(target=NFC.readNFC, args=(user_credentials, end_threads), name="Authentication")
        display = threading.Thread(target=LCD.update, args=(user_credentials, end_threads), name="Display")
        security = threading.Thread(target=SEC.secure, args=(user_credentials,TIMEOUT, end_threads), name="Security")
        bell = threading.Thread(target=BELL.ringer, args=(record_bell_event, end_threads), name="Bell")
        servo = threading.Thread(target=SERVO.servo, args=(user_credentials, end_threads), name="Servo Motor")
        logger = threading.Thread(target=LOGGER.log, args=(user_credentials, record_bell_event, end_threads), name="Logging")
        
        print('Starting threads')
        # Idealy each module would be encapsulated into 
        # their own classes. This was implemented with
        # the web_server which starts up in a thread when 
        # the start() method is called. There is a stop 
        # method that ends the web_server thread on keyboard
        # interrupt.
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
        print('Please wait, we are carefully and gracefully exiting threads')
        web_server.stop()
        end_threads[0] = True
        while NFC_reader.is_alive() or display.is_alive() or security.is_alive() or bell.is_alive() or servo.is_alive() or logger.is_alive():
            sleep(1)

        print('Finally Exiting')

if __name__ == '__main__':
    main()