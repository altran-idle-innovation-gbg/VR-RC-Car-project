import RPi.GPIO as GPIO
import pygame
import time
from pygame.locals import *
import re
import socket
import os
import json

"""
# ------------------- Accelerometer --------------------
host = ''
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
# ----------------- End Accelerometer -------------------------------
"""
# ------------------ Communication with phone ----------------
socket_path = '/tmp/uv4l.socket'

try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise

s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
s.bind(socket_path)
s.listen(1)
# ----------------- end communication with phone -----------------

# ------------------ GPIO INITIATION ------------------------

GPIO.setmode(GPIO.BOARD)  # Below 4 rows sets the output pins for motor control
GPIO.setup(7, GPIO.OUT)  # EN1 controls left hand side wheels (H-bridge connector J1 pin1)
GPIO.setup(11, GPIO.OUT)  # EN2 controls right hand side wheels (H-bridge connector J1 pin7)
GPIO.setup(13, GPIO.OUT)  # DIR1 LH True=Forward & False=Backward
GPIO.setup(15, GPIO.OUT)  # DIR2 RH True=Forward & False=Backward

GPIO.setup(12, GPIO.OUT)  # Sets the pin 12 as an output/signaling pin for the Servo
GPIO.setwarnings(False)
GPIO.output(7, False)
GPIO.output(11, False)

# ---------------- END GPIO INITIATION -----------------------

# -------------------- Variables -----------------------------
t = 0.05  # run time
servoStepLength = 0.5  # Set Step length for Servo
forward = False  # Constant to set the direction the wheels spin
backward = True  # Constant to set the direction the wheels spin
MAX_DC = 9.5
MIN_DC = 5.5
keycode_forward = [103]
keycode_backward = [108]
keycode_left = [105]
keycode_right = [106]
keycode_calibrate_forward = [28]
keycode_quit = ""
# ------------------- END Variables --------------------------

# ------------------- Start Car Class ------------------------


class Car(object):
    def __init__(self):
        self.drivingDirection = "stop"
        self.cameraDirection = 7.5
        self.cameraForward = 180.0

    def get_driving_direction(self):
        return self.drivingDirection

    def set_driving_direction(self, driving_direction):
        self.drivingDirection = driving_direction

    def get_camera_direction(self):
        return self.cameraDirection

    def set_camera_direction(self, camera_direction):
        if camera_direction < MIN_DC:
            self.cameraDirection = MIN_DC
        elif camera_direction > MAX_DC:
            self.cameraDirection = MAX_DC
        else:
            self.cameraDirection = camera_direction

    def set_camera_forward(self, camera_forward):
        self.cameraForward = camera_forward

    def get_camera_forward(self):
        return self.cameraForward

    def servo_turn_left(self):
        if self.cameraDirection >= MIN_DC + servoStepLength:
            self.cameraDirection -= servoStepLength
        else:
            print('Maximum Left turn acheived')

    def servo_turn_right(self):
        if self.cameraDirection <= MAX_DC - servoStepLength:
            self.cameraDirection += servoStepLength
        else:
            print('Maximum Right turn acheived')

    def calculate_duty_cycle(self, alpha):
        alpha_forward_diff1 = alpha - self.cameraForward
        if alpha_forward_diff1 < 0:
            alpha_forward_diff2 = 360.0 + alpha - self.cameraForward
        else:
            alpha_forward_diff2 = -360.0 + alpha - self.cameraForward
        if abs(alpha_forward_diff1) <= abs(alpha_forward_diff2):
            alpha_forward_diff = alpha_forward_diff1
        else:
            alpha_forward_diff = alpha_forward_diff2
        self.set_camera_direction(7.5-alpha_forward_diff*2.5/90.0)

# ------------------- End Car Class------------------------------

# ----------------- Servo on startup ----------------------------
servoPin = 12  # Servo signaling pin
pwm = GPIO.PWM(servoPin, 50)
pwm.start(7.5)  # Makes the servo point straight forward
time.sleep(0.5)  # The time for the servo to straighten forward
# ---------------- END Servo on startup -------------------------

# -------Define class with GPIO instructions for driving---------


def drive_forward():
    GPIO.output(7, False)  # EN1 Disable RH wheels to spin
    GPIO.output(11, False)  # EN2 Disable LH wheels to spin
    GPIO.output(13, forward)  # Enable RH wheels to spin forward
    GPIO.output(15, forward)  # Enable LH wheels to spin forward
    GPIO.output(7, True)  # EN1 Enable RH wheels to spin
    GPIO.output(11, True)  # EN2 Enable LH wheels to spin


def drive_backward():
    GPIO.output(7, False)  # EN1 Disable RH wheels to spin
    GPIO.output(11, False)  # EN2 Disable LH wheels to spin
    GPIO.output(13, backward)  # Enable RH wheels to spin backwards
    GPIO.output(15, backward)  # Enable LH wheels to spin backwards
    GPIO.output(7, True)  # EN1 Enable RH wheels to spin
    GPIO.output(11, True)  # EN2 Enable LH wheels to spin


def drive_left_pivot():
    GPIO.output(7, False)  # EN1 Disable RH wheels to spin
    GPIO.output(11, False)  # EN2 Disable LH wheels to spin
    GPIO.output(13, backward)  # Enabels RH wheels to spin forward
    GPIO.output(15, forward)  # Enabels LH wheels to spin backwards
    GPIO.output(7, True)  # EN1 Enables RH wheels to spin
    GPIO.output(11, True)  # EN2 Enables LH wheels to spin


def drive_right_pivot():
    GPIO.output(7, False)  # EN1 Disable RH wheels to spin
    GPIO.output(11, False)  # EN2 Enables LH wheels to spin
    GPIO.output(13, forward)  # Enabels RH wheels to spin backwards
    GPIO.output(15, backward)  # Enabels LH wheels to spin forward
    GPIO.output(7, True)  # EN1 Enables RH wheels to spin
    GPIO.output(11, True)  # EN2 Enables LH wheels to spin


def stop_all():
    GPIO.output(7, False)
    GPIO.output(11, False)
    GPIO.output(13, False)
    GPIO.output(15, False)


# -------END-Define class with GPIO instructions for driving---------

# --------------------- Driving direction list ----------------------

driving_direction_list = {'forward': drive_forward, 'backward': drive_backward,
                          'left': drive_left_pivot, 'right': drive_right_pivot, 'stop': stop_all}


# --------------------- End Driving Direction List ------------------

# ---------------------- Start joystick control ---------------------


def drive_direction(axis0, axis1):
    axis0 = int(round(axis0))
    axis1 = int(round(axis1))
    if axis0 == -1 and axis1 == 0:
        print ("Going Forward")
        return 'forward'
    elif axis0 == 1 and axis1 == 0:
        print ("Going Backward")
        return 'backward'
    elif axis1 == 1:
        print ("Going Left")
        return 'left'
    elif axis1 == -1:
        print ("Going Right")
        return 'right'
    else:
        print "stop"
        return 'stop'

# ----------------------- End Joystick control -------------------

# -----------------------Define quit game class ------------------


def stop_program():
    """shuts down all running components of program"""
    stop_all()
    pwm.stop()
    GPIO.cleanup()
    print ("Shutting down!")
'''
    try:
        joyStick.quit()
    except:
        pass
'''


# ---------------------END Define quit game class ----------------

# ------------------------ Initialize game mode ------------------

pygame.init()
pygame.joystick.init()
try:
    joyStick = pygame.joystick.Joystick(0)
    joyStick.init()
except:
    pass
screen = pygame.display.set_mode((240, 240))
pygame.display.set_caption('VR CAR')


# ------------------------ End Initialization -------------------

# ---------------- Main ------------------------


def main():
    """
    the main loop can be toggled between joystick and keyboard
    controls by pressing the <space> key. while using keyboard controls,
    speed can be set using number keys 1 - 9
    """
    print 'awaiting connection...'
    connection, client_address = s.accept()
    print client_address
    the_car = Car()
    stop = False
    alpha_degrees = 180
    check_things = 5
    while True:
        data_in_string = connection.recv(256)
        print data_in_string
        try:
            data_in_json = json.loads(data_in_string)
            if stop:
                break
            if data_in_json.get('do'):
                alpha_degrees = float(data_in_json.get('do').get('alpha'))
                gamma_degrees = float(data_in_json.get('do').get('gamma'))
                if gamma_degrees < 0:
                    alpha_degrees -= 180
                    if alpha_degrees < 0:
                        alpha_degrees += 360
                the_car.calculate_duty_cycle(alpha_degrees)
            elif data_in_json.get('keycodes'):
                if data_in_json.get('keycodes') == keycode_forward:
                    the_car.set_driving_direction('forward')
                    check_things = 0
                elif data_in_json.get('keycodes') == keycode_backward:
                    the_car.set_driving_direction('backward')
                    check_things = 0
                elif data_in_json.get('keycodes') == keycode_left:
                    the_car.set_driving_direction('left')
                    check_things = 0
                elif data_in_json.get('keycodes') == keycode_right:
                    the_car.set_driving_direction('right')
                    check_things = 0
                elif data_in_json.get('keycodes') == keycode_calibrate_forward:
                    the_car.set_camera_forward(alpha_degrees)
            if check_things > 4:
                the_car.set_driving_direction('stop')
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    stop = True

            driving_direction_list[the_car.get_driving_direction()]()
            pwm.ChangeDutyCycle(the_car.get_camera_direction())
            print the_car.get_camera_direction()
            check_things += 1
        except ValueError:
            if data_in_string == quit:
                stop = True

# ------------------------End Main---------------------------------------

if __name__ == "__main__":
    try:
        main()
    except:
        pass
    stop_program()
