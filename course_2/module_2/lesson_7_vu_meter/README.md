# vu_meter

Volume Unit meter (VU meter) is an application used to monitor the intensity of sound using ALSA programming interface
for linux. There are two variants of this application:

1. Using dB (decibels)
2. Using FFT (Fast Fourier Transform)

## Accredition
All the code of this project was written by [radhikap18](https://github.com/radhikap18) as part of the 96 Boards projects repo [here](https://github.com/96boards/projects). The original code can be found [here](https://github.com/96boards/projects/tree/master/vu_meter). We use his code under the [MIT License](https://opensource.org/licenses/MIT) the repository has set.

# Table of Contents
- [1) Using dB](#1-using-db)
- [2) Hardware Requirements](#2-hardware-requirements)
- [3) Package Dependencies](#3-package-dependencies)
- [4) Building and running](#4-building-and-running)
- [5) Conclusion](#5-conclusion)

# 1. Using dB:

Here, the intensity of sound is calculated by computing RMS value of sampled audio signal and converting to dB. The
implementation is straight forward and simple.

Link to blog: http://www.96boards.org/blog/96boards-vu-meter-part-1/

# 2. Hardware requirements:

1. [HiKey development board](http://www.96boards.org/product/hikey/)
2. [USB mic](https://www.adafruit.com/product/3367?gclid=Cj0KCQjwhrzLBRC3ARIsAPmhsnV7xmpPhkGgkUXuj0vmOFLwUCjxhiF1lbgvio7QglCJQwX9oMOCBvMaAs3YEALw_wcB)

# 3. Package Dependencies

1. ALSA library
```
$ sudo apt-get install libasound2-dev
```

# 4. Building and Running:

``` shell
$ git clone https://github.com/96boards/ucsd-coursera.git
$ cd course_2/module_2/vu_meter
$ make
$ aplay -l
$ ./bin plughw:1,0
```

Replace the Sound card info according to your device
According to this, plughw:DEVICE#, SUBDEVICE#
You find these numbers using "aplay -l"

# 5. Conclusion:

Running the executable causes progress bar to move according to the sound intensity.

## Using FFT:

Under development
