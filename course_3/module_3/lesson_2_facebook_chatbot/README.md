# Facebook Chatbot

Create a Facebook chatbot that communicates with clients.

# Table of Contents

- [1) Hardware](#1-hardware)
   - [1.1) Hardware requirements](#11-hardware-requirements)
   - [1.2) Hardware setup](#12-hardware-setup)
- [2) Software](#2-software) 
   - [2.1) Operating System](#21-operating-system)
   - [2.2) Package dependencies](#22-package-dependencies)
- [3) Additional Steps](#3-additional-steps)
   - [3.1) Additional Substeps](#31-additional-substeps)
   - [3.2) More Substeps](#32-more-substeps)
- [4) Execution](#4-execution)
- [5) Resources](#5-resources)



***

# 1) Hardware (Optional)

## 1.1 Hardware requirements

- [Dragonboard 410c](http://www.96boards.org/product/dragonboard410c/)
- [96Boards Compliant Power Supply](http://www.96boards.org/product/power/)

## 1.2 Hardware setup

- DragonBoard 410 is powered off
- Connect I/O devices (Monitor, Keyboard, etc...)
- Power on your DragonBoard 410c with 96Boards compliant power supply

# 2) Software

## 2.1 Operating System

- [Linaro Debian based OS (latest)](https://github.com/96boards/documentation/blob/master/ConsumerEdition/DragonBoard-410c/Downloads/Debian.md)

## 2.2 Package Dependencies

```shell
sudo apt-get update
sudo apt-get dist-upgrade

sudo apt-get install -y python-dev python-pip
pip install awscli boto3
```
# 3) Amazon Web Services Setup

#### Create an AWS account.
Go to [AWS](https://aws.amazon.com/). Click on 'Create an AWS Account'. Follow their steps.  

Note: It does require a credit card, however, most services with limits are free for 12 months.

## 3.1 Create an IAM User.


#### Substep

```
some code
```
## 3.2 Give User Permissions

#### Substep

Instructions.

```shell
code
```
## 3.2 Obtain Keys
- AWS Access Key ID
- AWS Secret Acess Key
# 4) Execution


#### Run the Code

```shell
python main.py
```

# 5) Resources
[Facebook Chatbot](http://docs.aws.amazon.com/lex/latest/dg/fb-bot-association.html)
[Facebook Application Quickstart](https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start)
