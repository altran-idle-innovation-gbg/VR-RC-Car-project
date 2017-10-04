import RPi.GPIO as GPIO
import pygame
import time
from time import sleep
import os
import sys
import math
from pygame.locals import *
import string
import re
import socket, traceback

# -------------------Accelerometer--------------------

host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
# ------------------- End Accelerometer -------------------------------

# -------------------- GPIO INITIATION ------------------------

GPIO.setmode(GPIO.BOARD)  # Below 4 rows just tells the RPi what theese pins are output pinns =(pins to send signals to the H-brige with)
GPIO.setup(7, GPIO.OUT)  # EN1 controls left hand side wheels (H-bridge connector J1 pin1)
GPIO.setup(11, GPIO.OUT)  # EN2 controls right hand side wheelsa (H-bridge connector J1 pin7)
GPIO.setup(13, GPIO.OUT)  # DIR1 LH True=Forward & False=Backward
GPIO.setup(15, GPIO.OUT)  # DIR2 RH True=Forward & False=Backward

GPIO.setup(12, GPIO.OUT)  # Sets the pin 12 as an output/signaling pin for the Servo
GPIO.setwarnings(False)
GPIO.output(7, False)
GPIO.output(11, False)

# ------------------ END GPIO INITIATION -----------------------

# -------------------Start Car Class-------------------------------
class Car(object):

    def __init__(self):
        self.drivingDirection = "stop"
        self.cameraDirection = 7.5

    def get_driving_direction(self):
        return self.drivingDirection

    def set_driving_direction(self, driving_direction):
        self.drivingDirection = driving_direction

    def get_camera_direction(self):
        return self.cameraDirection

    def set_camera_direction(self, camera_direction):
        self.cameraDirection = camera_direction

    def servo_turn_left(self):
        if self.cameraDirection >= 5.5 + servoStepLength:
            self.cameraDirection -= servoStepLength
        else:
            print('Maximum Left turn acheived')

    def servo_turn_right(self):
        if self.cameraDirection <= 9.5 - servoStepLength:
            self.cameraDirection += servoStepLength
            pwm.ChangeDutyCycle(DC)
        else:
            print('Maximum Right turn acheived')


# -------------------End Car Class------------------------------

# ------------- Servo on startup -------------------------------
servoPin = 12  # Servo signaling pin
pwm = GPIO.PWM(servoPin, 50)
pwm.start(7.5)  # Makes the servo point straight forward
time.sleep(0.5)  # The time for the servo to straighten forward
# ----------- END Servo on startup ------------------------------

# ------Variables--------

t = 0.05  # run time
DC = 7.5  # Servo Straight forward
servoStepLength = 0.5  # Set Step length for Servo
stop = False

# ---END Variables-------

# -------Define class with GPIO instructions for driving---------


def drive_forward():
    GPIO.output(7, False)  # EN1 Disable RH wheels to spin
    GPIO.output(11, False)  # EN2 Disable LH wheels to spin
    GPIO.output(13, True)  # Enable RH wheels to spin forward
    GPIO.output(15, True)  # Enable LH wheels to spin forward
    GPIO.output(7, True)  # EN1 Enable RH wheels to spin
    GPIO.output(11, True)  # EN2 Enable LH wheels to spin


def drive_backward():
    GPIO.output(7, False)  # EN1 Disable RH wheels to spin
    GPIO.output(11, False)  # EN2 Disable LH wheels to spin
    GPIO.output(13, False)  # Enable RH wheels to spin backwards
    GPIO.output(15, False)  # Enable LH wheels to spin backwards
    GPIO.output(7, True)  # EN1 Enable RH wheels to spin
    GPIO.output(11, True)  # EN2 Enable LH wheels to spin


def drive_left_pivot():
    GPIO.output(7, False)  # EN1 Disable RH wheels to spin
    GPIO.output(11, False)  # EN2 Disable LH wheels to spin
    GPIO.output(13, True)  # Enabels RH wheels to spin forward
    GPIO.output(15, False)  # Enabels LH wheels to spin backwards
    GPIO.output(7, True)  # EN1 Enables RH wheels to spin
    GPIO.output(11, True)  # EN2 Enables LH wheels to spin


def drive_right_pivot():
    GPIO.output(7, False)  # EN1 Disable RH wheels to spin
    GPIO.output(11, False)  # EN2 Enables LH wheels to spin
    GPIO.output(13, False)  # Enabels RH wheels to spin backwards
    GPIO.output(15, True)  # Enabels LH wheels to spin forward
    GPIO.output(7, True)  # EN1 Enables RH wheels to spin
    GPIO.output(11, True)  # EN2 Enables LH wheels to spin


# --- Stop motors --- #
def stop_all():
    GPIO.output(7, 0)
    GPIO.output(11, 0)
    GPIO.output(13, 0)
    GPIO.output(15, 0)
# --END Stop motors--##

# ---END-Define class with GPIO instructions for driving---------


# Define class with GPIO instructions for driving

# --------Servo Movements--------------

'''
def printit():
    while runner:

        runs = False

        message, address = s.recvfrom(8192)
        var = message.split()
        temp2 = str(var[3].strip())
        temp3 = re.sub('[^0-9.-]', '', temp2)
        print (temp3)
        acc = float(temp3)

        if -3 < acc < -1:
            runs = True
            acc2 = 5.5  # left
        elif 1 < acc < 3:
            runs = True
            acc2 = 9.5  # right
        elif -1 <= acc <= 1:
            runs = True
            acc2 = 7.5  # middle
        else:
            runs = False

        try:
            if runs:
                pwm.ChangeDutyCycle(acc2)  # Makes the servo turn
                print(acc2)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()

'''
#####----------------------END servo movement--------------------

# --------------------- Driving direction list ----------------------

driving_direction_list = {'forward': drive_forward, 'backward': drive_backward,
                        'left': drive_left_pivot, 'right': drive_right_pivot, 'stop': stop_all}

# --------------------- End Driving Direction List ------------------

## -------------------- Start joystick control ---------------------

def drive_direction(axis0, axis1):
    axis0 = int(round(axis0))
    axis1 = int(round(axis1))
    if axis0 == 0 and axis1 == -1:
        #the_car.set_driving_direction('forward')
        print ("Going Forward")
        return 'forward'
    elif axis0 == 0 and axis1 == 1:
        #the_car.set_driving_direction('backward')
        print ("Going Backward")
        return 'backward'
    elif axis0 == -1:
        #the_car.set_driving_direction('left')
        print ("Going LeftForward")
        return 'left'
    elif axis0 == 1:
        #the_car.set_driving_direction('right')
        print ("Going RightForward")
        return 'right'
    else:
        return 'stop'
'''   elif axis0 == -1 and axis1 == 1:
        driveLeftBackward()
        print ("Going LeftBackward")
    elif axis0 == 1 and axis1 == 1:
        driveRightBackward()
        print ("Going RightBackward")
    elif axis0 == -1 and axis1 == 0:
        driveLeftPivot()
        print ("LeftPivot")
    elif axis0 == 1 and axis1 == 0:
        driveRightPivot()
        print ("RightPivot")'''


## ------------------- End Joystick control -------------------

# ----------Define quit game class -----------------
def stop_program():
     """shuts down all running components of program"""

     try:
        joyStick.quit()
     except:
        pass

     stop_all()
     pwm.stop()
     GPIO.cleanup()
     print ("Shutting down!")


        # --------END Define quit game class ----------------
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

def main():
    '''the main loop can be toggled between joystick and keyboard
    controls by pressing the <space> key. while using keyboard controls,
    speed can be set using number keys 1 - 9'''
    the_car = Car()
    stop = False
    while True:
        if stop:
            break
        running = True
        runner = True
        lights = 0
        while running:
            time.sleep(.02)
            if stop:
                break
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    axis0 = joyStick.get_axis(0)
                    axis1 = joyStick.get_axis(1)
                    update_driving_direction = drive_direction(axis0, axis1)
                    the_car.set_driving_direction(update_driving_direction)
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1: #button C on joystick-VRBOX for camera turn LEFT
                        the_car.servo_turn_left()
                        print ("Camera turn left")
                    if event.button == 4: #button A on joystick-VRBOX for camera point STRAIGHT
                        the_car.set_camera_direction(7.5)
                        print ("Camera point straight forward")
                    if event.button == 3: #button D on joystick-VRBOX for camera turn RIGHT
                        the_car.servo_turn_right()
                        print ("Camera turn right")
                elif event.type == pygame.KEYDOWN:
                    if event.key == 32:
                        running = False
                        runner = False
                    elif event.key == K_ESCAPE:
                        stop = True

        stop_all()

        running = True
        while running:
            time.sleep(.02)
            if stop:
                break
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == 32:  # key <SPACE> Stop motors / Break
                        stop_all()
                    if event.key == K_w:  # key <W> Move forward
                        the_car.set_driving_direction('forward')
                        print(the_car.get_driving_direction())
                    if event.key == K_s:  # key <S> Move backward
                        the_car.set_driving_direction('backward')
                        print(the_car.get_driving_direction())
                    if event.key == K_a:  # key <A> Move left
                        the_car.set_driving_direction('left')
                        print(the_car.get_driving_direction())
                    if event.key == K_d:  # key <D> Move right
                        the_car.set_driving_direction('right')
                        print(the_car.get_driving_direction())

                    if event.key == K_q:  # key <Q> Turn servo left
                        the_car.set_camera_direction(5.5)
                    if event.key == K_r:  # key <R> Turn servo right
                        the_car.set_camera_direction(9.5)
                    if event.key == K_e:  # key <E> Turn servo straight forward
                        the_car.set_camera_direction(7.5)

                    if event.key == K_c:
                        the_car.servo_turn_left()
                        print('Camera Direction DC = ', the_car.get_camera_direction())
                    if event.key == K_v:
                        the_car.servo_turn_right()
                        print('Camera Direction DC = ', the_car.get_camera_direction())

                    if event.key == K_ESCAPE:  # key <Esc> QUIT
                        stop = True
                elif event.type == pygame.KEYUP:
                    the_car.set_driving_direction('stop')
                    print(the_car.get_driving_direction())

                driving_direction_list[the_car.get_driving_direction()]()
                pwm.ChangeDutyCycle(the_car.get_camera_direction())
                time.sleep(0.05)
try:
    main()
except:
    pass
stop_program()
