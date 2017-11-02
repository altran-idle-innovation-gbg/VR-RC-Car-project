# import RPi.GPIO as GPIO
import pigpio
import pygame
import time
from pygame.locals import *
import re
import socket
import os
import json

# ------------------ Communication with phone ----------------
""" Setup of the communication service through the webrtc server."""
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
""" This section declares and initialize the gpio pins """
pi = pigpio.pi()  # Setup pigpio connection to the raspberry pi
ENABLE_L_PIN = 4  # GPIO pin number for enabling left side wheels
ENABLE_R_PIN = 17  # GPIO pin number for enabling right side wheels
DIR_L_PIN = 27  # GPIO pin number for direction of left side wheels
DIR_R_PIN = 22  # GPIO pin number for direction of right side wheels
SERVO_PIN_Z_AXIS = 18  # GPIO pin number for Servo pin rotating around the z-axis
SERVO_PIN_ELEVATION = 19  # GPIO pin number for Servo pin changing the elevation angle

pi.set_mode(ENABLE_L_PIN, pigpio.OUTPUT)  # EN1 controls left hand side wheels (H-bridge connector J1 pin1)
pi.set_mode(ENABLE_R_PIN, pigpio.OUTPUT)  # EN2 controls right hand side wheels (H-bridge connector J1 pin7)
pi.set_mode(DIR_L_PIN, pigpio.OUTPUT)  # DIR1 LH True=Backward & False=Forward
pi.set_mode(DIR_R_PIN, pigpio.OUTPUT)  # DIR2 RH True=Backward & False=Forward
pi.set_mode(SERVO_PIN_Z_AXIS, pigpio.OUTPUT)  # Sets the physical pin 12 as an output/signaling pin for the Servo
pi.set_mode(SERVO_PIN_ELEVATION, pigpio.OUTPUT)  # Sets the physical pin 35 as an output/signaling pin for the Servo

pi.write(ENABLE_L_PIN, False)  # Set left side wheels to stop spinning.
pi.write(ENABLE_R_PIN, False)  # Set right side wheels to stop spinning.
# ---------------- END GPIO INITIATION -----------------------
# -------------------- Variables -----------------------------
"""This section initialize constants used through out the program"""
t = 0.05  # run time
servoStepLength = 0.5  # Set Step length for Servo
forward = False  # Constant to set the direction the wheels spin
backward = True  # Constant to set the direction the wheels spin
MAX_PW_ELEVATION = 2300  # set the maximum pulse width of the pulse width modulation
                         # for the Servo controlling elevation angle. Larger pulse width points the cameras downward
MIN_PW_ELEVATION = 1000  # set the minimum pulse width of the pulse width modulation
                        # for the Servo controlling elevation angle. Lower pulse width points the cameras upwards
START_PW_ELEVATION = 1000  # initialization value for the z-axis servo
MAX_PW_Z = 2250  # set the maximum pulse width of the pulse width modulation
                 # for the Servo controlling rotation around Z-axis
MIN_PW_Z = 750  # set the minimum pulse width of the pulse width modulation
                # for the Servo controlling rotation around Z-axis
START_PW_Z = 1500  # initialization value for the z-axis servo
keycode_forward = [103]  # set key code for driving forward
keycode_backward = [108]  # set key code for driving backward
keycode_left = [105]  # set key code for turning left
keycode_right = [106]  # set key code for turning right
keycode_calibrate_forward = [28]  # set key code for calibrating forward servo direction
quit_command = 'quit'  # Command sent through webRTC server to turn off program.
stop_command = 'stop'  # Command sent through webRTC server to sever connection to cellphone
# ------------------- END Variables --------------------------
# ------------------- Start Car Class ------------------------
"""The Car class is used to keep track of the car settings. 
   The car is initialized as standing still with camera direction forward"""


class Car(object):
    def __init__(self):
        """The car is initialized as standing still with camera direction forward"""
        self.drivingDirection = "stop"
        self.cameraDirection_Z = 1500
        self.cameraDirection_Elevation = 2000
        self.cameraForward = 180.0

    def get_driving_direction(self):
        """Returns the driving direction (String)"""
        return self.drivingDirection

    def set_driving_direction(self, driving_direction):
        """Set the driving direction (String): possible values: forward, backward, left, right and stop."""
        self.drivingDirection = driving_direction

    def get_camera_direction_z(self):
        """Returns the pulse width of the PWM signal that controls the servo rotating around the z-axis."""
        return self.cameraDirection_Z

    def get_camera_direction_elevation(self):
        """Returns the pulse width of the PWM signal that controls the servo controlling the elevation angle."""
        return self.cameraDirection_Elevation

    def set_camera_direction_z(self, camera_direction_z):
        """Set the pulse width of the PWM signal that controls the servo rotating around the z-axis (float).
           Checks if the pulse width is within the allowed pulse width length and otherwise sets it to the upper or
           lower limit. If within the allowed pulse width it rounds the number to the closest tens, since the RPI can
           only handle this resolution"""
        if camera_direction_z < MIN_PW_Z:
            self.cameraDirection_Z = MIN_PW_Z
        elif camera_direction_z > MAX_PW_Z:
            self.cameraDirection_Z = MAX_PW_Z
        else:
            self.cameraDirection_Z = round(camera_direction_z, -1)

    def set_camera_direction_elevation(self, camera_direction_elevation):
        """Set the pulse width of the PWM signal that controls the servo rotating around the z-axis. 
           Checks if the pulse width is within the allowed pulse width length and otherwise sets it to the upper or
           lower limit. If within the allowed pulse width it rounds the number to the closest tens, since the RPI can
           only handle this resolution"""
        if camera_direction_elevation < MIN_PW_ELEVATION:
            self.cameraDirection_Elevation = MIN_PW_ELEVATION
        elif camera_direction_elevation > MAX_PW_ELEVATION:
            self.cameraDirection_Elevation = MAX_PW_ELEVATION
        else:
            self.cameraDirection_Elevation = round(camera_direction_elevation, -1)

    def set_camera_forward(self, camera_forward):
        """Recalibrates which angle is considered forward around the z axis (float)."""
        self.cameraForward = camera_forward

    def get_camera_forward(self):
        """Returns which angle is considered forward (float)"""
        return self.cameraForward

    def calculate_new_pulse_widths(self, alpha, gamma):
        """Calculates and sets the pulse width of the servos. inputs: 1. alpha: the angle (degrees) around z-axis as
           taken from the phone. 2. gamma: elevation angle (degrees) as taken from the phone.
           The alpha angle is compared to the forward angle."""
        alpha_forward_diff1 = alpha - self.cameraForward
        gamma_diff = 90 - gamma
        if alpha_forward_diff1 < 0:
            alpha_forward_diff2 = 360.0 + alpha - self.cameraForward
        else:
            alpha_forward_diff2 = -360.0 + alpha - self.cameraForward

        if abs(alpha_forward_diff1) <= abs(alpha_forward_diff2):
            alpha_forward_diff = alpha_forward_diff1
        else:
            alpha_forward_diff = alpha_forward_diff2

        self.set_camera_direction_z(1500-alpha_forward_diff*750/90.0)
        self.set_camera_direction_elevation(2000.0+gamma_diff*1000.0/90.0)

# ------------------- End Car Class------------------------------
# ----------------- Servo on startup ----------------------------
"""The Servo is started, and later only the duty cycle is changed to
direct the cameras in different directions"""


def initialize_servo():
    pi.set_servo_pulsewidth(SERVO_PIN_Z_AXIS, START_PW_Z)  # Makes the servo point straight forward
    pi.set_servo_pulsewidth(SERVO_PIN_ELEVATION, START_PW_ELEVATION)  # Makes the servo point straight up
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
    pi.set_servo_pulsewidth(SERVO_PIN_Z_AXIS, 0)
    pi.set_servo_pulsewidth(SERVO_PIN_ELEVATION, 0)
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
                pi.set_servo_pulsewidth(SERVO_PIN_Z_AXIS, START_PW_Z)
                pi.set_servo_pulsewidth(SERVO_PIN_ELEVATION, START_PW_ELEVATION)
                time.sleep(1)
                pi.set_servo_pulsewidth(SERVO_PIN_Z_AXIS, 0)
                pi.set_servo_pulsewidth(SERVO_PIN_ELEVATION, 0)
                stop_all()
                connection.send('Connection aborted, will reconnect in 15s if call not hanged up.')
                connection.close()
                time.sleep(15)
                break
            data_in_string = connection.recv(256)
            try:
                data_in_json = json.loads(data_in_string)
                if data_in_json.get('do'):
                    alpha_degrees = float(data_in_json.get('do').get('alpha'))
                    gamma_degrees = float(data_in_json.get('do').get('gamma'))
                    if gamma_degrees < 0:
                        alpha_degrees -= 180
                        gamma_degrees += 180
                        if alpha_degrees < 0:
                            alpha_degrees += 360
                    the_car.calculate_new_pulse_widths(alpha_degrees, gamma_degrees)
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
                pi.set_servo_pulsewidth(SERVO_PIN_Z_AXIS, round(the_car.get_camera_direction_z(), -1))
                pi.set_servo_pulsewidth(SERVO_PIN_ELEVATION, round(the_car.get_camera_direction_elevation(), -1))
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
