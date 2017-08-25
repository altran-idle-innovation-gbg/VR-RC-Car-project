import RPi.GPIO as gpio
import time
def init():
    gpio.setmode(gpio.BOARD) #Below 4 rows just tells the RPi what theese pins are output pinns =(pins to send signals to the H-brige withgpio.setup(7,gpio.OUT)  #EN1 controls left hand side wheels (H-bridge connector J1 pin1)
    gpio.setup(7,gpio.OUT)  #EN1 controls left hand side wheels (H-bridge connector J1 pin1)
    gpio.setup(11,gpio.OUT) #EN2 controles right hand side wheelsa (H-bridge connector J1 pin7)
    gpio.setup(13,gpio.OUT) # DIR1 LH True=Forward & False=Backward
    gpio.setup(15,gpio.OUT) # DIR2 RH True=Forward & False=Backward

def forward(t):
    init()
    gpio.output(7, True)  # EN1 Enables LH wheels to spin
    gpio.output(11, True) # EN2 Enables RH wheels to spin
    gpio.output(13, True) # Enabels LH wheels to spin forward
    gpio.output(15, True) # Enabels RH wheels to spin forward
    time.sleep(t)
    gpio.cleanup()

def reverse(t):
    init()
    gpio.output(7, True)  # EN1 Enables LH wheels to spin
    gpio.output(11, True) # EN2 Enables RH wheels to spin
    gpio.output(13, False) # Enabels LH wheels to spin backwards
    gpio.output(15, False) # Enabels RH wheels to spin backwards
    time.sleep(t)
    gpio.cleanup()

def turnright(t):
    init()
    gpio.output(7, True)  # EN1 Enables LH wheels to spin
    gpio.output(11, False) # EN2 Enables RH wheels to spin
    gpio.output(13, True) # Enabels LH wheels to spin forward
    time.sleep(t)
    gpio.cleanup()

def turnleft(t):
    init()
    gpio.output(7, False)  # EN1 Enables LH wheels to spin
    gpio.output(11, True) # EN2 Enables RH wheels to spin
    gpio.output(15, True) # Enabels RH wheels to spin furward
    time.sleep(t)
    gpio.cleanup()

t=1    
forward(t)
reverse(t)
turnright(t)
turnleft(t)


gpio.cleanup()   

