import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD) #Below 4 rows just tells the RPi what theese pins are output pinns =(pins to send signals to the H-brige with)
servoPin=16 # Servo signaling pin
gpio.setup(servoPin, gpio.OUT) # Set the pin 16 as an output/signaling pin

pwm=gpio.PWM(servoPin,50)
pwm.start(7) # straight forward
for i in range(5,165): # The servo travels from 5 degrees to 165 degrees (I did not use 0-180 because it looked like it was too much for the gearbox)
    DC= 1./18.*(i)+2 # this is the formula/relation between Period and Deuty cycles (1 period=1/frequency =>1/50Hz=20ms, Period=%*Dutycycle)
    pwm.ChangeDutyCycle(DC)
    time.sleep(.05)
for i in range(165,5,-1):
    DC= 1./18.*(i)+2
    pwm.ChangeDutyCycle(DC)
    time.sleep(.05)
    
#pwm.start(7)# straight forward
#pwm.ChangeDutyCycle(2)# max to right
#pwm.ChangeDutyCycle(12) # max left

pwm.stop()
gpio.cleanup()
