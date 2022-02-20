from lib.PCF8574 import PCF8574_GPIO 
from lib.Adafruit_LCD1602 import Adafruit_CharLCD
from mfrc522 import SimpleMFRC522
from time import time, sleep

def setUp():
    # Setup NFC Reader
    reader = SimpleMFRC522()

    # Global Variables
    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
    # Create PCF8574 GPIO adapter.
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print ('I2C Address Error !')
            exit(1)

    mcp.output(3,1)         # Turn on the LCD backlight
    lcd = Adafruit_CharLCD(pin_rs=0,pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
    
    return [lcd, reader]

def destroy(lcd):
    print('Clearing LCD')
    # lcd.clear()
    messageUpdate(lcd,"Sleeping","")


first_line = ''
second_line = ''
def messageUpdate(lcd, first, second):
    global first_line, second_line

    if(first == first_line and second == second_line):
        return

    lcd.clear()
    lcd.message( first + '\n')
    lcd.message( second )
    
    first_line = first
    second_line = second
    

def update(lcd, user_credentials, kill_threads):
    lcd.begin(16,2)     # set number of LCD lines and columns
    
    while(not kill_threads[0]):
        sleep(1)
        if abs(user_credentials[2]-time()) > 5:
            messageUpdate(lcd, 'Please scan', 'your card.')
        elif user_credentials[3] == True:
            messageUpdate(lcd, "Welcome Home", str(user_credentials[1]) )
            
        else:
            messageUpdate(lcd, 'Unauthorized User', 'Please Wait')

    destroy(lcd)
    