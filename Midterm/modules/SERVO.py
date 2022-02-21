#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
OFFSET_DUTY = 0.5        # define pulse offset of servo
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY     # define pulse duty cycle for minimum angle of servo
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY    # define pulse duty cycle for maximum angle of servo
SERVO_DELAY_SEC = 0.001
SERVO_PIN = 24
permanent_unlock = False


def setup():
    global p
    GPIO.setmode(GPIO.BCM)         # use PHYSICAL GPIO Numbering
    GPIO.setup(SERVO_PIN, GPIO.OUT)   # Set servoPin to OUTPUT mode
    GPIO.output(SERVO_PIN, GPIO.LOW)  # Make servoPin output LOW level

    p = GPIO.PWM(SERVO_PIN, 50)     # set Frequence to 50Hz
    p.start(0)                     # Set initial Duty Cycle to 0
    
def servoWrite(angle):      # make the servo rotate to specific angle, 0-180 
    dc = SERVO_MIN_DUTY + (SERVO_MAX_DUTY - SERVO_MIN_DUTY) * angle / 180.0 # map the angle to duty cycle
    p.ChangeDutyCycle(dc)

def lock():
    for angle in range(0, 181, 1):   # make servo rotate from 0 to 180 deg
        servoWrite(angle)
        time.sleep(SERVO_DELAY_SEC)

def unlock():
    for angle in range(180, -1, -1): # make servo rotate from 180 to 0 deg
        servoWrite(angle)
        time.sleep(SERVO_DELAY_SEC)

def set_permanent_unlock(state):
    global permanent_unlock
    permanent_unlock = state

def servo(user_credentials, end_threads):
    global permanent_unlock
    setup()
    locked = False
    
    while(not end_threads[0]):
        if not permanent_unlock and not user_credentials[3]:
            if not locked:
                lock()
                locked = True
        elif locked:
            unlock()
            locked = False

        time.sleep(0.5)
    p.stop()
    print("Servo stopping")
