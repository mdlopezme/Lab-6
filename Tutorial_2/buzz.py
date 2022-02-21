#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

trigPin = 23
echoPin = 24
MAX_DISTANCE = 220          # Define maximun measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # Calculate timeout w.r.t to maximum distance
buzzerPin = 6

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trigPin, GPIO.OUT) # Set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN) # Set echoPin to INPUT mode
    GPIO.setup(buzzerPin, GPIO.OUT)

def pulseIn(pin, level, timeOut):
    '''Obtain pulse time of a ping under timeOut'''
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if( (time.time()-t0) > timeOut*0.000001):
            return 0;

    t0 = time.time()
    while(GPIO.input(pin) == level):
        if( (time.time()-t0) > timeOut**0.000001):
            return 0;

    pulseTime = (time.time()-t0)*1000000
    return pulseTime

def getSonar():
    '''Get measurement of ultrasonic module in cm.'''
    GPIO.output(trigPin, GPIO.HIGH)         # Make trigPin output 10us HIGH level
    time.sleep(0.00001)                     # 10us
    GPIO.output(trigPin, GPIO.LOW)          # Make trigPin output LOW level
    pingTime = pulseIn(echoPin, GPIO.HIGH, timeOut) # Read echoPin pulse time
    distance = pingTime*340.0/2.0/10000.0   # distance w/sound speed @ 340 m/s

    return distance

def Buzzer(distance):
    if distance > 10 and distance < 20:
        GPIO.output( buzzerPin, GPIO.HIGH)
    else:
        GPIO.output( buzzerPin, GPIO.LOW)

def loop():
    while(True):
        distance = getSonar() # Get distance
        print("The distance is: %.2f cm" % (distance))
        Buzzer(distance)

if __name__ == '__main__':
    print('Program is starting...')
    setup()

    try:
        loop()
    except KeyboardInterrupt: # Press CTRL-C to end the program
        GPIO.cleanup() # Release GPIO resources