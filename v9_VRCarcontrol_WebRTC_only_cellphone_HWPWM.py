import RPi.GPIO as GPIO
import pigpio
import pygame
import time
from pygame.locals import *
import re
import socket
import os
import json

# ------------------ Communication with phone ----------------
"""Setup of the communication servo through the webrtc server"""
socket_path = '/tmp/uv4l.socket'
try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise
s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
s.bind(socket_path)
s.listen(0)
# ----------------- end communication with phone -----------------
# ------------------ GPIO INITIATION ------------------------
pi = pigpio.pi()
ENABLE_L_PIN = 4
ENABLE_R_PIN = 17
DIR_L_PIN = 27
DIR_R_PIN = 22
SERVO_PIN = 18
pi.set_mode(ENABLE_L_PIN, pigpio.OUTPUT)  # EN1 controls left hand side wheels (H-bridge connector J1 pin1)
pi.set_mode(ENABLE_R_PIN, pigpio.OUTPUT)  # EN2 controls right hand side wheels (H-bridge connector J1 pin7)
pi.set_mode(DIR_L_PIN, pigpio.OUTPUT)  # DIR1 LH True=Backward & False=Forward
pi.set_mode(DIR_R_PIN, pigpio.OUTPUT)  # DIR2 RH True=Backward & False=Forward

pi.set_mode(SERVO_PIN, pigpio.OUTPUT)  # Sets the pin 12 as an output/signaling pin for the Servo
pi.write(ENABLE_L_PIN, False)
pi.write(ENABLE_R_PIN, False)
# ---------------- END GPIO INITIATION -----------------------
# -------------------- Variables -----------------------------
t = 0.05  # run time
servoStepLength = 0.5  # Set Step length for Servo
forward = False  # Constant to set the direction the wheels spin
backward = True  # Constant to set the direction the wheels spin
MAX_DC = 2250  # set boundary for maximum duty cycle for the Servo
MIN_DC = 750  # set boundary for minimum duty cycle for the Servo
keycode_forward = [103]  # set key code for driving forward
keycode_backward = [108]  # set key code for driving backward
keycode_left = [105]  # set key code for turning left
keycode_right = [106]  # set key code for turning right
keycode_calibrate_forward = [28]  # set key code for calibrating forward servo direction
quit_command = 'quit'
stop_command = 'stop'
# ------------------- END Variables --------------------------
# ------------------- Start Car Class ------------------------
"""The Car class is used to keep track of the car settings."""


class Car(object):
    def __init__(self):
        self.drivingDirection = "stop"
        self.cameraDirection = 1500
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

        self.set_camera_direction(1500-alpha_forward_diff*750/90.0)

# ------------------- End Car Class------------------------------
# ----------------- Servo on startup ----------------------------
"""The Servo is started, and later only the duty cycle is changed to
direct the cameras in different directions"""


def initialize_servo():
    pi.set_servo_pulsewidth(SERVO_PIN, 1500)  # Makes the servo point straight forward
    time.sleep(0.5)  # The time for the servo to straighten forward
# ---------------- END Servo on startup -------------------------
# -------Define class with GPIO instructions for driving---------
"""Functions to drive the Car. Because how the h-bridge is designed, the motors need to be
disabled before changing the driving directions of the motors."""


def drive_forward():
    pi.write(ENABLE_L_PIN, False)  # EN1 Disable RH wheels to spin
    pi.write(ENABLE_R_PIN, False)  # EN2 Disable LH wheels to spin
    pi.write(DIR_L_PIN, forward)  # Enable RH wheels to spin forward
    pi.write(DIR_R_PIN, forward)  # Enable LH wheels to spin forward
    pi.write(ENABLE_L_PIN, True)  # EN1 Enable RH wheels to spin
    pi.write(ENABLE_R_PIN, True)  # EN2 Enable LH wheels to spin


def drive_backward():
    pi.write(ENABLE_L_PIN, False)  # EN1 Disable RH wheels to spin
    pi.write(ENABLE_R_PIN, False)  # EN2 Disable LH wheels to spin
    pi.write(DIR_L_PIN, backward)  # Enable RH wheels to spin backwards
    pi.write(DIR_R_PIN, backward)  # Enable LH wheels to spin backwards
    pi.write(ENABLE_L_PIN, True)  # EN1 Enable RH wheels to spin
    pi.write(ENABLE_R_PIN, True)  # EN2 Enable LH wheels to spin


def drive_left_pivot():
    pi.write(ENABLE_L_PIN, False)  # EN1 Disable RH wheels to spin
    pi.write(ENABLE_R_PIN, False)  # EN2 Disable LH wheels to spin
    pi.write(DIR_L_PIN, backward)  # Enabels RH wheels to spin forward
    pi.write(DIR_R_PIN, forward)  # Enabels LH wheels to spin backwards
    pi.write(ENABLE_L_PIN, True)  # EN1 Enables RH wheels to spin
    pi.write(ENABLE_R_PIN, True)  # EN2 Enables LH wheels to spin


def drive_right_pivot():
    pi.write(ENABLE_L_PIN, False)  # EN1 Disable RH wheels to spin
    pi.write(ENABLE_R_PIN, False)  # EN2 Enables LH wheels to spin
    pi.write(DIR_L_PIN, forward)  # Enabels RH wheels to spin backwards
    pi.write(DIR_R_PIN, backward)  # Enabels LH wheels to spin forward
    pi.write(ENABLE_L_PIN, True)  # EN1 Enables RH wheels to spin
    pi.write(ENABLE_R_PIN, True)  # EN2 Enables LH wheels to spin


def stop_all():
    pi.write(ENABLE_L_PIN, False)
    pi.write(ENABLE_R_PIN, False)
    pi.write(DIR_L_PIN, False)
    pi.write(DIR_R_PIN, False)


# -------END-Define class with GPIO instructions for driving---------
# --------------------- Driving direction list ----------------------
"""The driving list is later used as a look up table to call the driving functions."""
driving_direction_list = {'forward': drive_forward, 'backward': drive_backward,
                          'left': drive_left_pivot, 'right': drive_right_pivot, 'stop': stop_all}
# --------------------- End Driving Direction List ------------------
# -----------------------Define quit game class ------------------


def stop_program():
    """shuts down all running components of program"""
    stop_all()
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    pi.stop()
    print ("Shutting down!")


# ---------------------END Define quit game class ----------------
# ---------------- Main ------------------------


def main():
    """
    the main loop can be toggled between joystick and keyboard
    controls by pressing the <space> key. while using keyboard controls,
    speed can be set using number keys 1 - 9
    """
    the_car = Car()
    alpha_degrees = 180.0
    iteration_control = 0
    turn_off_program = False
    averaging_duty_cycle = [180.0, 180.0, 180.0]
    while True:
        if turn_off_program:
            break
        print 'awaiting connection...'
        connection, client_address = s.accept()
        print client_address
        initialize_servo()
        stop = False
        while True:
            if stop:
                pi.set_servo_pulsewidth(SERVO_PIN, 0)
                stop_all()
                connection.send('Connection aborted, will reconnect in 15s if call not hanged up.')
                connection.close()
                time.sleep(15)
                break
            data_in_string = connection.recv(256)
            try:
                data_in_json = json.loads(data_in_string)
                print data_in_json
                if data_in_json.get('do'):
                    alpha_degrees = float(data_in_json.get('do').get('alpha'))
                    gamma_degrees = float(data_in_json.get('do').get('gamma'))
                    if gamma_degrees < 0:
                        alpha_degrees -= 180
                        if alpha_degrees < 0:
                            alpha_degrees += 360
                    averaging_duty_cycle.pop(0)
                    averaging_duty_cycle.append(alpha_degrees)
                    alpha_degrees = round(sum(averaging_duty_cycle)/len(averaging_duty_cycle), 1)
                    the_car.calculate_duty_cycle(alpha_degrees)
                elif data_in_json.get('keycodes'):
                    if data_in_json.get('keycodes') == keycode_forward:
                        the_car.set_driving_direction('forward')
                        iteration_control = 5
                    elif data_in_json.get('keycodes') == keycode_backward:
                        the_car.set_driving_direction('backward')
                        iteration_control = 5
                    elif data_in_json.get('keycodes') == keycode_left:
                        the_car.set_driving_direction('left')
                        iteration_control = 2
                    elif data_in_json.get('keycodes') == keycode_right:
                        the_car.set_driving_direction('right')
                        iteration_control = 2
                    elif data_in_json.get('keycodes') == keycode_calibrate_forward:
                        the_car.set_camera_forward(alpha_degrees)
                if iteration_control <= 0:
                    the_car.set_driving_direction('stop')
                    iteration_control = 0

                driving_direction_list[the_car.get_driving_direction()]()
                pi.set_servo_pulsewidth(SERVO_PIN,round(the_car.get_camera_direction(), -1))
                iteration_control -= 1
            except ValueError:
                if data_in_string == quit_command:
                    stop = True
                    turn_off_program = True
                elif data_in_string == stop_command:
                    stop = True
# ------------------------End Main---------------------------------------

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print e
    stop_program()
