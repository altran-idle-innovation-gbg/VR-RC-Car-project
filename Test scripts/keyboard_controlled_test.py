import RPi.GPIO as gpio
import time
import socket
 
UDP_IP = "10.46.2.129"
UDP_PORT = 10042

#sock = socket.socket(socket.AF_INET, # Internet

#socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP, UDP_PORT))

gpio.setmode(gpio.BOARD) #Below 4 rows just tells the RPi what theese pins are output pinns =(pins to send signals to the H-brige with)
gpio.setup(7,gpio.OUT)  #EN1 controls left hand side wheels (H-bridge connector J1 pin1)
gpio.setup(11,gpio.OUT) #EN2 controles right hand side wheelsa (H-bridge connector J1 pin7)
gpio.setup(13,gpio.OUT) # DIR1 LH True=Forward & False=Backward
gpio.setup(15,gpio.OUT) # DIR2 RH True=Forward & False=Backward

gpio.output(7,False)
gpio.output(11,False)
t=1 #run time
running = True
a = raw_input("\t PRESS P TO ABORT \n Press any key to start")

print(''' \t Press 'w' to move forward \n
         Press 'a' to move left \n
         Press 'd' to move right \n
         Press 's' to move back \n
                 ''')
while running:
    a = raw_input('Press a key to move the robot')
    if a.lower() == 'w':
        gpio.output(7, True)  # EN1 Enables LH wheels to spin
        gpio.output(11, True) # EN2 Enables RH wheels to spin
        gpio.output(13, True) # Enabels LH wheels to spin forward
        gpio.output(15, True) # Enabels RH wheels to spin forward
        time.sleep(t)
        gpio.cleanup()
        print("workiwng forward")

    if a.lower() == 'a':
        gpio.output(7, True)  # EN1 Enables LH wheels to spin
        gpio.output(11, False) # EN2 Enables RH wheels to spin
        gpio.output(13, True) # Enabels LH wheels to spin forward
        time.sleep(t)
        gpio.cleanup()
        print("working left")

    if a.lower() == 's':
        gpio.output(7, True)  # EN1 Enables LH wheels to spin
        gpio.output(11, True) # EN2 Enables RH wheels to spin
        gpio.output(13, False) # Enabels LH wheels to spin backwards
        gpio.output(15, False) # Enabels RH wheels to spin backwards
        time.sleep(t)
        gpio.cleanup()
        print("working backwards")

    if a.lower() == 'd':
        gpio.output(7, False)  # EN1 Enables LH wheels to spin
        gpio.output(11, True) # EN2 Enables RH wheels to spin
        gpio.output(15, True) # Enabels RH wheels to spin furward
        time.sleep(t)
        gpio.cleanup()
        print("working right")

    if a.lower() == 'p':
        gpio.output(7,False)
        gpio.output(11,False)
        running = False
        
print('Stopping gracefully')
gpio.cleanup()
