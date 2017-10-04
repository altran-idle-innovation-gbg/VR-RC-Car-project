import RPi.GPIO as gpio
import pygame
import time
from time import sleep
import os
import sys
import math
from pygame.locals import *
###-------------------Accelerometer--------------------
import string
import re
import socket, traceback

host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
###--------------------------------------------------


# IP_ADDRESS = "192.168.0.2" # ip address of host used for video stream
# RASPICAM_ON = "raspivid -t 999999 -w 1280 -h 720 -sa -50 -br 60 -co 20 -fps 24 -b 3000000 -o - | gst-launch-1.0 -e -vvv fdsrc ! h264parse ! rtph264pay pt=96 config-interval=5 ! udpsink host=" + IP_ADDRESS + " port=8160&"
# RASPICAM_OFF = "sudo killall -9 gst-launch-1.0"
PHOTOS_DIR = "/home/pi/Desktop/Tank_photos"  # save photos to a any directory
SNAP_PHOTO = "raspistill -w 1920 -h 1080 -t 500 -o " + PHOTOS_DIR + "/"
IMAGE_NUMBERS_TXT_FILE = "image_numbers.txt"  # text file to append number to 'image.jpg'
EMAIL_TO = "altran.innovation.gbg@gmail.com"
###### GPIO INITIATION #######
gpio.setmode(
    gpio.BOARD)  # Below 4 rows just tells the RPi what theese pins are output pinns =(pins to send signals to the H-brige with)
gpio.setup(7, gpio.OUT)  # EN1 controls left hand side wheels (H-bridge connector J1 pin1)
gpio.setup(11, gpio.OUT)  # EN2 controles right hand side wheelsa (H-bridge connector J1 pin7)
gpio.setup(13, gpio.OUT)  # DIR1 LH True=Forward & False=Backward
gpio.setup(15, gpio.OUT)  # DIR2 RH True=Forward & False=Backward
gpio.setup(16, gpio.OUT)  # Sets the pin 16 as an output/signaling pin for the Servo
gpio.setwarnings(False)
gpio.output(7, False)
gpio.output(11, False)
###### Servo on startup #########
servoPin = 16  # Servo signaling pin

pwm = gpio.PWM(servoPin, 50)
pwm.start(9)  # Makes the servo point straight forward

time.sleep(1)  # The time for the servo to straighten forward
pwm.stop()  # Stop the servo
###### END Servo on startup ######

t = 0.05  # run time


# ---------------------------------------------------
# Define class with GPIO instructions for driving

def servoLeft():
    servoPin = 16  # Servo signaling pin
    pwm = gpio.PWM(servoPin, 50)
    pwm.start(1)  # Makes the servo point left
    time.sleep(1)  # The time for the servo to turn left
    pwm.stop()  # Stop the servo


def servoStraight():
    servoPin = 16  # Servo signaling pin
    pwm = gpio.PWM(servoPin, 50)
    pwm.start(6.5)  # Makes the servo point straight forward
    time.sleep(1)  # The time for the servo to point forward
    pwm.stop()  # Stop the servo


def servoRight():
    servoPin = 16  # Servo signaling pin
    pwm = gpio.PWM(servoPin, 50)
    pwm.start(13)  # Makes the servo point right
    time.sleep(1)  # The time for the servo to turn right
    pwm.stop()  # Stop the servo


def driveForward():
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True)  # EN2 Enable LH wheels to spin
    gpio.output(13, True)  # Enable RH wheels to spin forward
    gpio.output(15, True)  # Enable LH wheels to spin forward
    time.sleep(t)


def driveBackward():
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True)  # EN2 Enable LH wheels to spin
    gpio.output(13, False)  # Enable RH wheels to spin backwards
    gpio.output(15, False)  # Enable LH wheels to spin backwards
    time.sleep(t)


def driveLeftForward():
    gpio.output(7, True)  # EN1 Enables RH wheels to spin
    gpio.output(11, False)  # EN2 Disable LH wheels to spin
    gpio.output(13, True)  # Enabels RH wheels to spin forward
    gpio.output(15, False)  # Enabels LH wheels to spin backwards
    time.sleep(t)


def driveRightForward():
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, True)  # EN2 Enables LH wheels to spin
    gpio.output(13, False)  # Enabels RH wheels to spin backwards
    gpio.output(15, True)  # Enabels LH wheels to spin forward
    time.sleep(t)


def driveLeftBackward():
    gpio.output(7, True)  # EN1 Enables RH wheels to spin
    gpio.output(11, False)  # EN2 Disable LH wheels to spin
    gpio.output(13, False)  # Enabels RH wheels to spin backwards
    gpio.output(15, False)  # Enabels LH wheels to spin backwards
    time.sleep(t)


def driveRightBackward():
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, True)  # EN2 Enables LH wheels to spin
    gpio.output(13, False)  # Enabels RH wheels to spin backwards
    gpio.output(15, False)  # Enabels LH wheels to spin forward
    time.sleep(t)


def driveLeftPivot():
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True)  # EN2 Enable LH wheels to spin
    gpio.output(13, True)  # Enable LH wheels to spin backward
    gpio.output(15, False)  # Enable RH wheels to spin forward
    time.sleep(t)


def driveRightPivot():
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True)  # EN2 Enable LH wheels to spin
    gpio.output(13, False)  # Enable RH wheels to spin forward
    gpio.output(15, True)  # Enable LH wheels to spin backwards
    time.sleep(t)


def printit():
    #####------------------------servo movement--------------------
    while runner:

        runs = False

        message, address = s.recvfrom(8192)

        var = message.split()
        temp2 = str(var[3].strip())
        temp3 = re.sub('[^0-9.-]', '', temp2)

        print (temp3)

        acc = float(temp3)

        if (-3 < acc < -1):
            runs = True
            acc2 = 4  # left
        elif (1 < acc < 3):
            runs = True
            acc2 = 11  # right
        elif (-1 <= acc <= 1):
            runs = True
            acc2 = 8  # middle
        else:
            runs = False

        try:
            if runs:
                servoPin = 16  # Servo signaling pin
                pwm = gpio.PWM(servoPin, 50)
                pwm.start(acc2)  # Makes the servo turn
                time.sleep(1)  # The time for the servo to turn
                pwm.stop()  # Stop the servo
                print(acc2)


        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()


#####----------------------END servo movement--------------------

##    def stopDriving():
##        gpio.output(7,False) # EN1 Disable RH wheels to spin
##        gpio.output(11,False) # EN2 Disable LH wheels to spin
##        running = False

def stopAll():
    gpio.output(7, 0)
    gpio.output(11, 0)
    gpio.output(13, 0)
    gpio.output(15, 0)


def driveDirection(axis0, axis1):
    axis0 = int(round(axis0))
    axis1 = int(round(axis1))
    if axis0 == 0 and axis1 == -1:
        driveForward()
        print ("Going Forward")
    if axis0 == 0 and axis1 == 1:
        driveBackward()
        print ("Going Backward")
    if axis0 == -1 and axis1 == 0:
        driveLeftForward()
        print ("Going LeftForward")
    if axis0 == 1 and axis1 == 0:
        driveRightForward()
        print ("Going RightForward")
    if axis0 == -1 and axis1 == 1:
        driveLeftBackward()
        print ("Going LeftBackward")
    if axis0 == 1 and axis1 == 1:
        driveRightBackward()
        print ("Going RightBackward")
    if axis0 == -1 and axis1 == 0:
        driveLeftPivot()
        print ("LeftPivot")
    if axis0 == 1 and axis1 == 0:
        driveRightPivot()
        print ("RightPivot")
    if axis0 == 0 and axis1 == 0:
        stopAll()


# ---------------------------------------------------


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

"""this sets up the GPIO pins (GPIO.BOARD) to be used
with a TB6612FNG motor controller as labeled"""
##AIN1 = 3 # left side motor
##AIN2 = 5 # left side motor
##BIN1 = 8 # right side motor
##BIN2 = 10 # right side motor
##PWMA = 11 # left side PWM
##PWMB = 12 # right side PWM
##STBY = 7 # standby pin

speed = 50


def getFileNum(txt_file):
    """returns a sequential number that reads and writes to
    image_numbers.txt"""

    read_number = open(txt_file, 'r')
    num = int(read_number.read()) + 1
    read_number.close()

    write_number = open(txt_file, 'w')
    str_num = str(num)
    write_number.write(str_num)
    write_number.close()

    read_number = open(txt_file, 'r')
    number = read_number.read()
    read_number.close()

    return number


def getFileName(txt_file):
    """returns a sequential file name to photos taken"""

    number = str(getFileNum(txt_file))
    return "image_" + number + ".jpg"


def takePic(file_name):
    os.system(RASPICAM_OFF)
    time.sleep(.5)
    os.system(SNAP_PHOTO + file_name)
    os.system(RASPICAM_ON)
    return file_name


def emailPic(email):
    file_name = takePic(getFileName(IMAGE_NUMBERS_TXT_FILE))
    os.system("/home/pi/email_attach.py " + PHOTOS_DIR + file_name + " " + email + "&")
    print file_name + " emailed to " + email


def main():
    '''the main loop can be toggled between joystick and keyboard
    controls by pressing the <space> key. while using keyboard controls,
    speed can be set using number keys 1 - 9'''

    #    os.system(RASPICAM_ON)
    stop = False
    while True:
        if stop == True:
            break
        running = True
        runner = True
        lights = 0
        while running:
            time.sleep(.02)
            if stop == True:
                break
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    axis0 = joyStick.get_axis(0)
                    axis1 = joyStick.get_axis(1)
                    driveDirection(axis0, axis1)
                ##                elif event.type == pygame.JOYBUTTONDOWN:
                ##                    if event.button == 1: #button C on joystick-VRBOX for camera turn LEFT
                ##                        servoLeft()
                ##                        print ("Camera turn left")
                ##                    if event.button == 4: #button A on joystick-VRBOX for camera point STRAIGHT
                ##                        servoStraight()
                ##                        print ("Camera point straight forward")
                ##                    if event.button == 3: #button D on joystick-VRBOX for camera turn RIGHT
                ##                        servoRight()
                ##                        print ("Camera turn right")
                elif event.type == pygame.KEYDOWN:
                    if event.key == 32:
                        running = False
                        runner = False
                    elif event.key == K_ESCAPE:
                        stop = True

        stopAll()

        running = True
        speed = 350
        while running:
            time.sleep(.02)
            if stop == True:
                break
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in MOVE_IT:  # keys <w> <a> <s> <d>
                        MOVE_IT[event.key](speed)
                    elif event.key == 102:  # key <f>
                        lights = headLights(lights)
                    elif event.key in SPEED:  # keys <1 - 9>
                        speed = SPEED[event.key]
                    elif event.key == 99:  # key <c>
                        takePic(getFileName(IMAGE_NUMBERS_TXT_FILE))
                    elif event.key == 118:  # key <v>
                        emailPic(EMAIL_TO)
                    elif event.key == 32:  # key <space>
                        running = False
                        runner = False
                    elif event.key == K_ESCAPE:  # key <escape>
                        stop = Truewsw
                elif event.type == pygame.KEYUP:
                    stopAll()


def quit():
    """shuts down all running components of program"""

    try:
        joyStick.quit()
    except:
        pass
    stopAll()
    os.system(RASPICAM_OFF)
    print "Goodbye!"


main()
quit()
