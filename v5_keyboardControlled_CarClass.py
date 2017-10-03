########################################################################                                                                  
# This example is for controlling the GoPiGo robot from a mouse scroll                          
# http://www.dexterindustries.com/GoPiGo/                                                                
########################################################################
import struct
import sys
from gopigo import *

import RPi.GPIO as gpio
import pygame
import time
from time import sleep
import os
import math
from pygame.locals import *

import string
import re
import socket, traceback

###-------------------Accelerometer-----------------------
host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
###-----------------END Accelerometer---------------------

###-------------------- GPIO INITIATION ------------------------
gpio.setmode(gpio.BOARD) #Below 4 rows just tells the RPi what theese pins are output pinns =(pins to send signals to the H-brige with)
gpio.setup(7,gpio.OUT)  #EN1 controls left hand side wheels (H-bridge connector J1 pin1)
gpio.setup(11,gpio.OUT) #EN2 controles right hand side wheelsa (H-bridge connector J1 pin7)
gpio.setup(13,gpio.OUT) # DIR1 LH True=Forward & False=Backward
gpio.setup(15,gpio.OUT) # DIR2 RH True=Forward & False=Backward
gpio.setup(12,gpio.OUT) # Sets the pin 12 as an output/signaling pin for the Servo
gpio.setwarnings(False)
gpio.output(7,False)
gpio.output(11,False)
###------------------ END GPIO INITIATION -----------------------

###-------------------Start Car Class-------------------------------
class Car(object):
    drivingDirection=""
    cameraDirection=7.5

    def __init__(self):
        self.drivingDirection="stop"
        self.cameraDirection=7.5
    
    def getDrivingDirection(self):
        return self.drivingDirection

    def setDrivingDirection(self,drivingDirection):
        self.drivingDirection = drivingDirection
    
    def getCameraDirection(self):
        return self.cameraDirection

    def setCameraDirection(self,cameraDirection):
        self.cameraDirection=cameraDirection
    def servoTurnLeft(self):
        if self.cameraDirection>=5.5+servoStepLength:
            self.cameraDirection-=servoStepLength
        else:
            print('Maximum Left turn acheived')
 
    def servoTurnRight(self):
        if self.cameraDirection<=9.5-servoStepLength:
            self.cameraDirection+=servoStepLength
            pwm.ChangeDutyCycle(DC)
        else:
            print('Maximum Right turn acheived')


###-------------------End Car Class------------------------------

###------------- Servo on startup -------------------------------
servoPin = 12 # Servo signaling pin

pwm = gpio.PWM(servoPin,50)
pwm.start(7.5) # Makes the servo point straight forward

time.sleep(0.5)   # The time for the servo to straighten forward
#pwm.stop()      # Stop the servo
###----------- END Servo on startup ------------------------------

###------Variables--------

t = 0.05 #run time
DC = 7.5  # Servo Straight forward
servoStepLength=0.5  # Set Step length for Servo

###---END Variables-------

###-------Define class with GPIO instructions for driving---------
def driveForward():
    gpio.output(7, False)  # EN1 Enable RH wheels to spin
    gpio.output(11, False) # EN2 Enable LH wheels to spin
    gpio.output(13, True) # Enable RH wheels to spin forward
    gpio.output(15, True) # Enable LH wheels to spin forward
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True) # EN2 Enable LH wheels to spin
    
def driveBackward():
    gpio.output(7, False)  # EN1 Enable RH wheels to spin
    gpio.output(11, False) # EN2 Enable LH wheels to spin
    gpio.output(13, False) # Enable RH wheels to spin backwards
    gpio.output(15, False) # Enable LH wheels to spin backwards
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True) # EN2 Enable LH wheels to spin
    
def driveLeftForward():
    gpio.output(7, False)  # EN1 Enables RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, True) # Enabels RH wheels to spin forward
    gpio.output(15, False) # Enabels LH wheels to spin backwards
    gpio.output(7, True)  # EN1 Enables RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    
def driveRightForward():
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, False) # EN2 Enables LH wheels to spin
    gpio.output(13, False) # Enabels RH wheels to spin backwards
    gpio.output(15, True) # Enabels LH wheels to spin forward
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, True) # EN2 Enables LH wheels to spin

##--- Stop motors ---##
def stopAll():
    gpio.output(7, 0)
    gpio.output(11, 0)
    #gpio.output(13, 0)
    #gpio.output(15, 0)
##--END Stop motors--##
###---END-Define class with GPIO instructions for driving---------

###----------Define quit game class -----------------
def quit():
    """shuts down all running components of program"""
    try:
        joyStick.quit()
    except:
        pass
    stopAll()
    pwm.stop()
    gpio.cleanup()
    print ("Shutting down!")
###--------END Define quit game class ----------------

###--------Initialize pyGame -------------------
pygame.init()
pygame.joystick.init()
try:
    joyStick = pygame.joystick.Joystick(0)
    joyStick.init()
except:
    pass
screen = pygame.display.set_mode((240, 240))
pygame.display.set_caption('VR CAR')
###------ END Initialize pyGame ----------------

##----keyboard codes for pygame
##----http://thepythongamebook.com/en:glossary:p:pygame:keycodes

##--------------------- Driving direction list ----------------------
drivingDirectionList = {'forward': driveForward, 'backward':driveBackward,
      'left':driveLeftForward, 'right':driveRightForward, 'stop':stopAll}


##--------------------- keyboard steering -------------------------
def main():
    theCar = Car()
    runs = True

    while runs:
        time.sleep(.02)
        if stop == True:
            break
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 32: # key <SPACE> Stop motors / Break
                    stopAll()
                if event.key == K_w: # key <W> Move forward
                    theCar.setDrivingDirection('forward')
                    print(theCar.getDrivingDirection())
                    #driveForward()
                if event.key == K_s: # key <S> Move backward
                    theCar.setDrivingDirection('backward')
                    print(theCar.getDrivingDirection())
                    #driveBackward()
                if event.key == K_a: # key <A> Move left
                    theCar.setDrivingDirection('left')
                    print(theCar.getDrivingDirection())
                    #driveLeftForward()
                if event.key == K_d: # key <D> Move right
                    theCar.setDrivingDirection('right')
                    print(theCar.getDrivingDirection())
                    #driveRightForward()

                if event.key == K_q: # key <Q> Turn servo left
                    theCar.setCameraDirection(5.5)
                    #servoLeft()
                if event.key == K_r: # key <R> Turn servo right
                    theCar.setCameraDirection(9.5)
                    #servoRight()
                if event.key == K_e: # key <E> Turn servo straight forward
                    theCar.setCameraDirection(7.5)
                    #servoStraight()
                
                if event.key == K_c:
                    theCar.servoTurnLeft()
                    print('Camera Direction DC = ',theCar.getCameraDirection())
                if event.key == K_v:
                    theCar.servoTurnRight()
                    print('Camera Direction DC = ',theCar.getCameraDirection())

                if event.key == K_ESCAPE: # key <Esc> QUIT
                    quit()
            elif event.type == pygame.KEYUP:
                theCar.setDrivingDirection('stop')
                print(theCar.getDrivingDirection())
                #stopAll()
            drivingDirectionList[theCar.getDrivingDirection()]()
            pwm.ChangeDutyCycle(theCar.getCameraDirection())
            time.sleep(0.05)
##-------------------- END keyboard steering -----------------------                

if __name__ == "__main__":
    main()
    quit() 

