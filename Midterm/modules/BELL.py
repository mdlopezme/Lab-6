#!/usr/bin/env python3
from gpiozero import LED, Button
from time import sleep

led = LED(17)       # define LED pin according to BCM Numbering
button = Button(18) # define Button pin according to BCM Numbering

def onButtonPressed(): 
    global bell_press_has_been_log
    led.on()
    bell_press_has_been_log[0] = False
    # print("Button Pressed, Bell is Ringing >>>")
    
def onButtonReleased():
    global bell_press_has_been_log
    led.off()
    # print("Button Released, Stopping Bell <<<")

bell_press_has_been_log = []
def ringer(bell_press_has_been_log_pass, kill_threads):
    global bell_press_has_been_log
    bell_press_has_been_log = bell_press_has_been_log_pass

    button.when_pressed = onButtonPressed
    button.when_released = onButtonReleased

    while(not kill_threads[0]):
        sleep(1)