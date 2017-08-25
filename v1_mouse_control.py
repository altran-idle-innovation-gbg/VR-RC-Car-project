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
###-------------------Accelerometer-----------------------
import string
import re
import socket, traceback

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
gpio.setup(16,gpio.OUT) # Sets the pin 16 as an output/signaling pin for the Servo
gpio.setwarnings(False)
gpio.output(7,False)
gpio.output(11,False)
###------------------ END GPIO INITIATION -----------------------

###------------- Servo on startup -------------------------------
servoPin = 16 # Servo signaling pin

pwm = gpio.PWM(servoPin,50)
pwm.start(6.5) # Makes the servo point straight forward

time.sleep(1)   # The time for the servo to straighten forward
#pwm.stop()      # Stop the servo
###----------- END Servo on startup ------------------------------

###------Variables--------

t = 0.05 #run time

###---END Variables-------

###-------Define class with GPIO instructions for driving---------
def servoLeft():
    servoPin = 16 # Servo signaling pin
    pwm = gpio.PWM(servoPin,50)
    pwm.start(8) # Makes the servo point left
    time.sleep(1)   # The time for the servo to turn left
    #pwm.stop()      # Stop the servo
    
def servoStraight():
    servoPin = 16 # Servo signaling pin
    pwm = gpio.PWM(servoPin,50)
    pwm.start(11) # Makes the servo point straight forward
    time.sleep(1)   # The time for the servo to point forward
    #pwm.stop()      # Stop the servo

def servoRight():
    servoPin = 16 # Servo signaling pin
    pwm = gpio.PWM(servoPin,50)
    pwm.start(2) # Makes the servo point right
    time.sleep(1)   # The time for the servo to turn right
    #pwm.stop()      # Stop the servo

def driveForward():
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True) # EN2 Enable LH wheels to spin
    gpio.output(13, True) # Enable RH wheels to spin forward
    gpio.output(15, True) # Enable LH wheels to spin forward
    time.sleep(t)
    
def driveBackward():
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True) # EN2 Enable LH wheels to spin
    gpio.output(13, False) # Enable RH wheels to spin backwards
    gpio.output(15, False) # Enable LH wheels to spin backwards
    time.sleep(t)
    
def driveLeftForward():
    gpio.output(7, True)  # EN1 Enables RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, True) # Enabels RH wheels to spin forward
    gpio.output(15, False) # Enabels LH wheels to spin backwards
    time.sleep(t)
    
def driveRightForward():
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, True) # EN2 Enables LH wheels to spin
    gpio.output(13, False) # Enabels RH wheels to spin backwards
    gpio.output(15, True) # Enabels LH wheels to spin forward
    time.sleep(t)

##--- Stop motors ---##
def stopAll():
    gpio.output(7, 0)
    gpio.output(11, 0)
    gpio.output(13, 0)
    gpio.output(15, 0)
##--END Stop motors--##
###---END-Define class with GPIO instructions for driving---------

####-----------Define class for servo movement --------------------    
def printit():
    while 1:
        try:
            print("1st")

            print "Press Enter to servo"
            b=raw_input()	#Wait for an input to start
            
            message, address = s.recvfrom(8192)
            print(message)
            
            var = message.split()
            temp2 = str(var[3].strip())
            temp3 = re.sub('[^0-9.-]', '', temp2)
            
            print("3rd")
            print (temp3)

            acc = float(temp3)

            if (-3 < acc < -1):
                runs = True
                acc2 = 4    # left
            elif (1 < acc < 3):
                runs = True
                acc2 = 11   # right
            elif (-1 <= acc <= 1):
                runs = True
                acc2 = 8    # middle
            else:
                runs = False
            print("4th")
            if runs:
                servoPin = 16 # Servo signaling pin
                pwm = gpio.PWM(servoPin,50)
                pwm.start(acc2) # Makes the servo turn
                time.sleep(1)   # The time for the servo to turn
                pwm.stop()      # Stop the servo
                print(acc2)
            print("5th")

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()
####----------- END Define class for servo movement ----------------
print("6th")
###----------Define quit game class -----------------
def quit():
    """shuts down all running components of program"""

    try:
        joyStick.quit()
    except:
        pass
    stop = True
    stopAll()
    gpio.cleanup()
    print ("Shutting down!")
###--------END Define quit game class ----------------

###------ Initialize pyGame --------------
pygame.init()
pygame.joystick.init()
try:
    joyStick = pygame.joystick.Joystick(0)
    joyStick.init()
except:
    pass
screen = pygame.display.set_mode((240, 240))
pygame.display.set_caption('VR CAR')
## print ("testDISPLAY")
###--- END Initialize pyGame --------------

########################### MOUSE MOVEMENT #################################
#Open the stream of data coming from the mouse
file = open( "/dev/input/mice", "rb" );
speed=150

debug = 0	#Print raw values when debugging

#Parse through the fata coming from mouse
#Returns: 	[left button pressed,
#		middle button pressed,
#		right button pressed,
#		change of position in x-axis,
#		change of position in y-axis]
def getMouseEvent():
	buf = file.read(3)
	button = ord( buf[0] )
	bLeft = button & 0x1
	bMiddle = ( button & 0x4 ) > 0
	bRight = ( button & 0x2 ) > 0
	x,y = struct.unpack( "bb", buf[1:] )
	if debug:
		print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) )
	return [bLeft,bMiddle,bRight,x,y]
	

flag=0
print "Press Enter to start"
a=raw_input()	#Wait for an input to start
set_speed(speed)
stop()
while( 1 ):
	[l,m,r,x,y]=getMouseEvent()	#Get the inputs from the mouse
	if debug:
		print l,m,r,x,y
	print x,"\t",y
	
	#If there is a signinficant mouse movement Up (positive y-axis)
	if y >20:
                print("FWD")
                driveForward()  #Move forward

	#If there is a signinficant mouse movement Down (negative y-axis)
	elif y<-20:
                print("BWD")
                driveBackward() #Move Back

	#If there is a signinficant mouse movement Left (positive x-axis)
	elif x<-20:
                print("LEFT")
                driveLeftForward()  #Move left

	#If there is a signinficant mouse movement Right (negative x-axis)
	elif x>20:
                print("RIGHT")
                driveRightForward() #Move Right

	#Stop the GoPiGo if left mouse button pressed
	if m:
                print("STOP!")
                stopAll()

        #Servo turn right and straighten out if right mouse button pressed
	if r:
                print("Servo straight")
                servoRight()
                
        #Servo turn right and straighten out if right mouse button pressed
	if l:
                print("Servo turn left")
                servoLeft()
                
        #printit() ## doesn't work - fix it
                
	time.sleep(.01)

	for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE: # key <escape>
                        quit()
                elif event.type == pygame.KEYUP:
                    if event.key == K_ESCAPE: # key <escape>
                        quit()

######################## END MOUSE MOVEMENT #################################
