#!/usr/bin/env python3
from gpiozero import LED, Button
from time import sleep

led = LED(17)       # define LED pin according to BCM Numbering
button = Button(18) # define Button pin according to BCM Numbering

def onButtonPressed(): 
    global record_bell_event
    led.on()
    record_bell_event[0] = True
    # print("Button Pressed, Bell is Ringing >>>")
    
def onButtonReleased():
    global record_bell_event
    led.off()
    # print("Button Released, Stopping Bell <<<")

record_bell_event = []
def ringer(bell_event, end_threads):
    global record_bell_event
    record_bell_event = bell_event

    button.when_pressed = onButtonPressed
    button.when_released = onButtonReleased

    while(not end_threads[0]):
        sleep(1)