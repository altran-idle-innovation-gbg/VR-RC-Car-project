#-------------------Accelerometer-------------------------
import RPi.GPIO as gpio
import string
import re
import socket, traceback

host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
#----------------------------------------------------------

gpio.setmode(gpio.BOARD) #Below 4 rows just tells the RPi what theese pins are output pinns =(pins to send signals to the H-brige with)
servoPin=16 # Servo signaling pin
gpio.setup(servoPin, gpio.OUT) # Set the pin 16 as an output/signaling pin

##--------------Set servo straight---------------##
pwm=gpio.PWM(servoPin,50)
pwm.start(7) # straight forward
##--------------Set servo straight---------------##

running = True
while running:
    message, address = s.recvfrom(8192)
            
    var = message.split()
    temp2 = str(var[3].strip())
    temp3 = re.sub('[^0-9-]', '', temp2)
    temp4 = int(temp3)

    if(temp4 > 1000):
        for z in range(0,4):
            val = 8 + z
    elif(temp4 < -1000):
        for z in range(0,3):
            val = 4 - z
    else:
        val = 6

    print (val)

    pwm.ChangeDutyCycle(val)

pwm.stop()
gpio.cleanup()

    ##-------------- ---------------##
##    for i in range(0,20):
##        desiredPosition=int(temp3)
##        DC= 1./18.*(desiredPosition)+2
##        print(DC)
##        pwm.ChangeDutyCycle(DC)
    ##-------------- ---------------##
