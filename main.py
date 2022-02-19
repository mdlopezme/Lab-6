#!/usr/bin/env python3
import modules.NFC as NFC
import modules.LCD as LCD
import modules.BELL as BELL
import modules.SEC as SEC
import modules.SERVO as SERVO
import modules.LOGGER as LOGGER
import modules.WEBSERVER as WEBSERVER

from time import time, sleep
import threading
import RPi.GPIO as GPIO

def main():
    print('Starting Program')

    [lcd, reader] = LCD.setUp()
    TIMEOUT = 5
    user_credentials = [0, '', time()-TIMEOUT, False, True ]
    ringer_info =[ False, time()-TIMEOUT, True ]

    try:
        authentication = threading.Thread(target=NFC.readNFC, args=(reader,user_credentials, TIMEOUT))
        display = threading.Thread(target=LCD.update, args=(lcd, user_credentials))
        bell = threading.Thread(target=BELL.ringer, args=(ringer_info,))
        servo = threading.Thread(target=SERVO.act, args=(user_credentials, TIMEOUT))
        logger = threading.Thread(target=LOGGER.log, args=(user_credentials, ringer_info, TIMEOUT))
        web_server = threading.Thread(target=WEBSERVER.main)

        authentication.start()
        display.start()
        bell.start()
        servo.start()
        logger.start()
        web_server.start()

    except KeyboardInterrupt:
        LCD.destroy(lcd)
        GPIO.cleanup()

if __name__ == '__main__':
    main()