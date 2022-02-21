Moises Lopez: A14156109

Olivier Rogers: A16069362

# Lab 6 Midterm

# HARDware

### Servo Module

The purpose of this module is to lock and unlock the door.

Writing Schematics:

![Screen Shot 2022-02-20 at 2.35.24 PM.png](images/Screen%20Shot%202022-02-20%20at%202.35.24%20PM.png?fileId=19790#mimetype=image%2Fpng&hasPreview=true)

### Bell Module

The purpose of this module is to ring the bell when the button is press. The schematics show a LED for feedback, but for our demonstration. Please replace the LED for a passive buzzer.

Writing Schematics:

![Screen Shot 2022-02-20 at 2.34.23 PM.png](images/Screen%20Shot%202022-02-20%20at%202.34.23%20PM.png?fileId=19764#mimetype=image%2Fpng&hasPreview=true)

### LCD Module

The purpose of this module is to show messages to the user.

The display has three different states.

1. (User authenticated successfully) Displays, 'Welcome home, $USER'. Where $USER is the full name of the authenticated user.
2. ( User authentication was unsuccessful) Displays, 'Unauthenticated user, please wait...'
3. (Idle state) Display, 'Please scan your card'

This module uses the driver `Adafruit_LCD1602` located in folder `lib`

Writing Schematics:

![Screen Shot 2022-02-20 at 2.36.20 PM.png](images/Screen%20Shot%202022-02-20%20at%202.36.20%20PM.png?fileId=19773#mimetype=image%2Fpng&hasPreview=true)![Screen Shot 2022-02-20 at 2.36.37 PM.png](images/Screen%20Shot%202022-02-20%20at%202.36.37%20PM.png?fileId=19781#mimetype=image%2Fpng&hasPreview=true)

### NFC Module

The purpose of this module is to read the NFC cards for user id and username. Also creates a time stamps, sets a bool that represents whether the use was authenticated, and another bool to false that represents that the current information has not been written to mysql.

This modules use the Simple MFRC522 driver for reading the NFC.

The driver can be found [here](https://github.com/pimylifeup/MFRC522-python/blob/master/mfrc522/SimpleMFRC522.py).

Writing Schematics

**SDA** connects to **CE0** on your extension board (Board pin 24)

**SCK** connects to **SCLK** on your extension board (Board pin 23)

**MOSI** connects to **MOSI** on your extension board (Board pin 19)

**MISO** connects to **MISO** on your extension board (Board pin 21)

**IRQ** is not used, so skip this.

**GND** is connected to **ground**, which can be on your ground rail or any of the cobbler pins marked GND (Board Pin 6 or 39 for example)

**RST** connects to GPIO 25 on Adafruit cobbler (Board pin 22)

**3.3V** connects to your **positive rail** (or you can connect to Board pin 1)

![ioctfig2.png](images/ioctfig2.png?fileId=19804#mimetype=image%2Fpng&hasPreview=true)

## Software

### Environment

Provides system specific information for the logger module (database info) and the NFC module (NFC id's).

### Init-DB Module

The purpose of this module is to make a Smart\_Home database.

And make two tables within that database.

1. User\_Auth (Logs all attempts that a user tries to authenticate: success or unsuccessful )
2. Bell\_Rings (Makes a timestamp for all the times the door bell was pressed)

### Logger Module

The purpose of this module is to log user authentication attempts and log whenever anyone pressed the door bell to mysql database.

### Security Module

The purpose of this module is to set the unlocked boolean from True to False after the a time period set my user. In order words, the amount of time for the door to re-lock after unlocking it.

### Webserver Module

Uses Pyramid to host a web interface for the device. A log of NFC scans and bell rings can be searched and filtered by days. In addition, the door access logs can be filtered by user. On page load, a query is sent to get all the user names which are then used to populate the select options.

There is an input option on the web interface that provides a choice between auto-lock and unlocked.

## Tutorial 1: Setup Raspberry Pi

Setting up the Raspberry Pi is similar to setting up a headless linux machine, except the imaging tool from [raspberrypi](https://www.raspberrypi.com/software/) makes it even easier by setting up wifi and ssh in the image.

Setting up SQL was nearly identical to that on my system with the main difference being the package manager used (apt on the pi and pacman on my system).

We decided to stick with ssh for logging into the raspberrypi, since we are both used to the linux cli and VS Code works nicely over ssh.

| ![Olivier Lab 5 Challenge](images/T1_Oli.png) | |:--- | | *Challenge 1 from Lab 5 (Olivier), logged in over ssh and running the server app. The browser loads the website from host suffix 100 on the LAN. The user workstation uses suffix 14.* |

## Tutorial 2: Basic I/O on Raspberry Pi

In this tutorial, we learned how to program and use the raspberry to read values from the GPIO. It was really fun to see how this works in the raspberry pi because we have only done this type of stuffs in Arduino.