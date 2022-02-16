#!/usr/bin/env python3
import modules.NFC as NFC
import modules.LCD as LCD
import modules.BELL as BELL
import modules.SEC as SEC
import modules.SERVO as SERVO
import modules.LOGGER as LOGGER
import web_server.WEBSERVER as WEBSERVER

from time import time, sleep
import threading
import RPi.GPIO as GPIO

def main():
    print('Starting Program')

    [lcd, reader] = LCD.setUp()
    timeOut = 5
    user_credentials = [0, '', time()-timeOut, False, True ]
    ringer_info =[ False, time()-timeOut, True ]

    try:
        authentication = threading.Thread(target=NFC.readNFC, args=(reader,user_credentials, timeOut))
        display = threading.Thread(target=LCD.update, args=(lcd, user_credentials))
        bell = threading.Thread(target=BELL.ringer, args=(ringer_info,))
        security = threading.Thread(target=SEC.secure, args=(user_credentials,timeOut))
        servo = threading.Thread(target=SERVO.act, args=(user_credentials, timeOut))
        logger = threading.Thread(target=LOGGER.log, args=(user_credentials, ringer_info, timeOut))
        web_server = threading.Thread(target=WEBSERVER.main)

        authentication.start()
        display.start()
        bell.start()
        security.start()
        servo.start()
        logger.start()
        web_server.start()

        # while(True):
        #     # print(user_credentials)
        #     print(ringer_info)
        #     sleep(0.1)
    except KeyboardInterrupt:
        LCD.destroy(lcd)
        GPIO.cleanup()

if __name__ == '__main__':
    main()