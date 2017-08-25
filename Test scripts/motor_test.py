import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD) #Below 4 rows just tells the RPi what theese pins are output pinns =(pins to send signals to the H-brige with)
gpio.setup(7,gpio.OUT)  #EN1 controls left hand side wheels (H-bridge connector J1 pin1)
gpio.setup(11,gpio.OUT) #EN2 controles right hand side wheelsa (H-bridge connector J1 pin7)
gpio.setup(13,gpio.OUT) # DIR1 LH True=Forward & False=Backward
gpio.setup(15,gpio.OUT) # DIR2 RH True=Forward & False=Backward

##gpio.output(7, True)  # EN1 Enables LH wheels to spin
##gpio.output(11, True) # EN2 Enables RH wheels to spin
##

##gpio.output(13, True) # Enabels LH wheels to spin forward
##gpio.output(15, True) # Enabels RH wheels to spin forward
##time.sleep(1) # determines that the wheels will spin for 2s
##
##gpio.output(13, False) # Enabels LH wheels to spin backwards
##gpio.output(15, False) # Enabels RH wheels to spin backwards
##time.sleep(1)

gpio.output(7, False) # Dissabel RH wheels from spinning
gpio.output(11, True) 

gpio.output(13, True)
gpio.output(15, False) 
time.sleep(1)
##
##gpio.output(13, False)
##gpio.output(15, True)
##time.sleep(1)
##
##gpio.output(7, True)  # Enabels LH wheels to spin
##gpio.output(11, False) # Dissabel RH wheels from spinning
##
##gpio.output(13, True)
##gpio.output(15, False)
##time.sleep(1)
##
##gpio.output(13, False)
##gpio.output(15, True)
##time.sleep(1)
##
##gpio.output(7, False)  # EN1 Disabels LH wheels to spin
##gpio.output(11, False) # EN2 Disabels RH wheels to spin

gpio.cleanup()   

