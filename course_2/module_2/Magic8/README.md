# Magic 8 Ball
The Magic 8 Ball application displays messages on the LCD when the touch sensor module is tapped.
There are 20 statements out of which any one can appear randomly at each tap on the sensor. So ask away!

## Accredition
All the code of this project was written by [radhikap18](https://github.com/radhikap18) as part of the 96 Boards projects repo [here](https://github.com/96boards/projects). The original code can be found [here](https://github.com/96boards/projects/tree/master/magic8). We use his code under the [MIT License](https://opensource.org/licenses/MIT) the repository has set.

# Table of Contents
- [1) Hardware](#1-hardware)
   - [1.1) Hardware Requirements](#11-hardware-requirements)
   - [1.2) Hardware Setup](#12-hardware-setup)
- [2) Software](#2-software) 
   - [2.1) Operating System](#21-operating-system)
   - [2.2) Package Dependencies](#22-package-dependencies)
- [3) Building and Running](#3-building-and-running)
- [4) Conclusion](#4-conclusion)

# 1. Hardware
   
## 1.1 Hardware requirements:

1. [DragonBoard 410c](http://www.96boards.org/product/dragonboard410c/)
2. [Power Supply](https://www.amazon.com/Adapter-Regulated-Supply-Copper-String/dp/B015G8DZK2)
3. [Sensors Mezzanine](http://www.96boards.org/product/sensors-mezzanine/)
4. [Micro USB Cable](https://www.amazon.com/AmazonBasics-USB-Male-Micro-Cable/dp/B01EK87A82/ref=sr_1_3?ie=UTF8&qid=1497618343&sr=8-3&keywords=micro%2Busb&th=1)
5. [Grove-LCD 16x2 RGB Backlight](https://www.seeedstudio.com/Grove-LCD-RGB-Backlight-p-1643.html)
6. [Grove Touch Sensor Module](https://www.seeedstudio.com/Grove-Touch-Sensor-p-747.html)

## 1.2 Hardware Setup:
To begin, connect the Sensors Mezzanine board onto the DragonBoard via the low-speed expansion connector on both boards. Use the Grove Universal 4 pin cables to connect the LCD to I2C0 and the Touch sensor module onto GPIO G3. You can find an image of the setup in the images folder. That’s it! We’re all set to run our application.

# 2. Software

## 2.1 Operating System

- [Linaro Debian based OS (latest)](https://github.com/96boards/documentation/blob/master/ConsumerEdition/DragonBoard-410c/Downloads/Debian.md)

## 2.2 Package Dependencies

1. MRAA Library
```
$ sudo apt-get install libupm-dev
```
2. UPM Library
```
$ sudo apt-get install libmraa-dev
```

# 3. Building and Running:

```shell
$ git clone https://github.com/96boards/ucsd-coursera.git
$ cd course_2/module_2/Magic8
$ make
$ ./magic8
```

# 4. Conclusion:

When the executable is run, the application displays an initial message on the LCD and waits for the sensor to be tapped.
With each tap, a new statement is displayed. These statements can be modified by the user in the code.
