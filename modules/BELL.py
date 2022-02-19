from pickletools import read_stringnl_noescape_pair
from gpiozero import LED, Button
from time import time, sleep

led = LED(21)       # define LED pin according to BCM Numbering
button = Button(20) # define Button pin according to BCM Numbering

def onButtonPressed(): 
    global ringer_info
    led.on()
    ringer_info[0] = True
    ringer_info[1] = time()
    ringer_info[2] = False
    # print("Button Pressed, Bell is Ringing >>>")
    
def onButtonReleased():
    global ringer_info
    led.off()
    # print("Button Released, Stopping Bell <<<")

ringer_info = [ False, time()-5]
def ringer(ringer_info_pass, kill_threads):
    global ringer_info
    ringer_info = ringer_info_pass

    button.when_pressed = onButtonPressed
    button.when_released = onButtonReleased

    while(not kill_threads[0]):
        sleep(1)