# Morse Code Reader

The Morse Code Reader project implements a DragonBoard version of an effective method of communication.
Through varying how long the user touches the touch sensor, the LCD backlight will output different letters,
eventually creating a cohesive message. The project goes through some of the basic concepts like connecting
the Sensors Mezzanine board with the DragonBoard, interfacing an LCD and a touch sensor with the board and 
installing the necessary libraries.

## Accredition
The main code of the morse code reader was written by [Grant Winney](https://github.com/grantwinney) as part of his [52-Weeks-of-Pi](https://github.com/grantwinney/52-Weeks-of-Pi) series. The original code can be found [here](https://github.com/grantwinney/52-Weeks-of-Pi/tree/master/02-Send-Morse-Code-Via-Button-Click). We use his code under the [MIT License](https://opensource.org/licenses/MIT) he has set for his repository.

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

## 1.2 Hardware Setup:

First, connect the Sensors Mezzanine board onto the DragonBoard via the low-speed expansion connector on both boards. Use the Grove Universal 4 pin cables to connect the LCD to I2C0 and the touch sensor to (whatever). You can find the images of the hardware setup in the images folder. That¿s it! We¿re all set to run our application.

# 2. Software

## 2.1 Operating System

- [Linaro Debian based OS (latest)](https://github.com/96boards/documentation/blob/master/ConsumerEdition/DragonBoard-410c/Downloads/Debian.md)

## 2.2 Package Dependencies
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
$ cd course_2/Module2/Morse_Code 																											$ python Transmitter.py																										
```																												


# 4. Conclusion:

When the program is executed, the user is provided with a brief guide on
Morse Code. The user is then prompted to touch the sensor in order to create
the first symbol of the morse code. This will continue until there is a period
of inactivity, which signifies that all the symbols for the first letter have
been received. Times and validity of every touch response will be displayed in
standard output. In order to exit the program, press any button.
