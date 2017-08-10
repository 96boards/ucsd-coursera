# Alarm Clock

The Alarm Clock is exactly what it's name says it is. It uses the LCD display to tell time. Uses buttons and potentiometer to set modes and to set the alarm time.

# Table of Contents
- [1) Hardware](#1-hardware)
   - [1.1) Hardware Requirements](#11-hardware-requirements)
   - [1.2) Hardware Setup](#12-hardware-setup)
- [2) Software](#2-software) 
   - [2.1) Operating System](#21-operating-system)
   - [2.2) Package Dependencies](#22-package-dependencies)
- [3) Building and running](#3-building-and-running)
- [4) Conclusion](#4-conclusion)

# 1. Hardware

## 1.1 Hardware Requirements:

1. [DragonBoard 410c](http://www.96boards.org/product/dragonboard410c/)
2. [Power Supply](https://www.amazon.com/Adapter-Regulated-Supply-Copper-String/dp/B015G8DZK2)
2. [Sensors Mezzanine](http://www.96boards.org/product/sensors-mezzanine/)
3. [Grove-LCD 16x2 RGB Backlight and a grove cable](https://www.seeedstudio.com/Grove-LCD-RGB-Backlight-p-1643.html)
4. [Grove Touch Sensor and a grove cable](https://www.seeedstudio.com/Grove-Touch-Sensor-p-747.html)
5. [Grove Button and a grove cable](https://www.seeedstudio.com/Grove-Button-p-766.html)
6. [Grove Rotary Angle Sensor and a grove cable](https://www.seeedstudio.com/Grove-Rotary-Angle-Sensor-p-770.html)
7. [Grove Buzzer](https://www.seeedstudio.com/Grove-Buzzer-p-768.html)

## 1.2 Hardware Setup:

First, connect the Sensors Mezzanine board onto the DragonBoard via the low-speed expansion connector on both boards. Use the Grove Universal 4 pin cables to connect the LCD to I2C0, the touch sensor, the button, the buzzer, and the rotary sensor to (whatever). You can find the images of the hardware setup in the images folder. That¿s it! We¿re all set to run our application.

# 2. Software

## 2.1 Operating System

- [Linaro Debian based OS (latest)](https://github.com/96boards/documentation/blob/master/ConsumerEdition/DragonBoard-410c/Downloads/Debian.md)

## 2.2 Package Dependencies
Tool Packages
```
$ sudo apt-get install arduino-mk arduino git build-essential autoconf libtool swig3.0 python-dev nodejs-dev cmake pkg-config libpcre3-dev
$ sudo apt-get clean
```

MRAA Library
```
$ sudo apt-get install libmraa-dev
```

UPM Library
```
$ sudo apt-get install libupm-dev
```

# 3. Building and Running:

```
$ git clone https://github.com/96boards/ucsd-coursera.git    
$ cd ucsd-coursera	
$ cd course_2/Module2/Morse_Code/	
$ make upload reset_stty
																												
$ python clock.py																										
```																												


# 4. Conclusion:
When the program is executed the current time will be shown on the LCD display. Pressing the button once, shows when the current alarm is set to. Prsesing it a second time, allows the user to change the alarm time's hours. Pressing a third time, allows the user to change the minutes of the alarm. Pressing it the last and fourth time, returns the display to show the current time.
