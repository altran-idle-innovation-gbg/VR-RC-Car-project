import RPi.GPIO as gpio
import pygame
import time
import os
import sys
import math
import string
import socket, traceback
from pygame.locals import *

###### GPIO INITIATION #######
gpio.setmode(gpio.BOARD) # Below row just tells the RPi what theese pins are output pins =(pins to send signals to the H-brige with)
gpio.setup(16,gpio.OUT) # Sets the pin 16 as an output/signaling pin for the Servo
gpio.setwarnings(False)

###### Servo on startup #########
servoPin = 16 # Servo signaling pin

## mh = Adafruit_MotorHAT(addr=0x60)
pwm = gpio.PWM(servoPin,50)

def turnOffMotors():

    pwm.stop() 
    #mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    #mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    #mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    #mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    #atexit.register(turnOffMotors)

# myMotor = mg.getMotor(1)

host="10.46.2.129"

port=5555

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

s.bind((host, port))

temp1=0

while 1:

        message, address = s.recvfrom(8192)

        print message

        var1 = message

        var2=var1.split(',')

        temp2=var2[2].strip(',')

        print temp2

        temp3 = float(temp2)

    if (temp3>5):

        # myMotor.run(Adafruit_MotorHAT.BACKWARD)
        # myMotor.setSpeed(40)
        # time.sleep(0.03)
        # myMotor.run(Adafruit_MotorHAT.RELEASE)
        # print "Rotate"
        
        servoPin = 16 # Servo signaling pin
        pwm = gpio.PWM(servoPin,50)
        pwm.start(1) # Makes the servo point left
        time.sleep(1)   # The time for the servo to turn left
        pwm.stop()      # Stop the servo
        print "Rotate left"
        

    elif (temp3<-5):

        # myMotor.run(Adafruit_MotorHAT.BACKWARD)
        # myMotor.setSpeed(40)
        # time.sleep(0.03)
        # myMotor.run(Adafruit_MotorHAT.RELEASE)
        # print "Rotate"

        servoPin = 16 # Servo signaling pin
        pwm = gpio.PWM(servoPin,50)
        pwm.start(13) # Makes the servo point right
        time.sleep(1)   # The time for the servo to turn right
        pwm.stop()      # Stop the servo
