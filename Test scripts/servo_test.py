import pigpio
import time
'''
gpio.setmode(gpio.BOARD) #Below 4 rows just tells the RPi what theese pins are output pinns =(pins to send signals to the H-brige with)
servoPin=12 # Servo signaling pin
gpio.setup(servoPin, gpio.OUT) # Set the pin 16 as an output/signaling pin

pwm=gpio.PWM(servoPin,50)
pwm.start(7) # straight forward
for i in range(0,20):
    desiredPosition=input("Where do you want the servo? 5-160 ")
    DC= 1./36.0*(desiredPosition)+5.0
    print(DC)
    pwm.ChangeDutyCycle(DC)
print(DC)
pwm.stop()
gpio.cleanup()
'''
'''
RPIO.setmode(RPIO.BOARD)
servo = RPIO.PWM.servo()
servo.set_servo(12,1500)
time.sleep(10)
servo.stop_servo(12)
'''
servopin = 18

pi = pigpio.pi()
pi.set_mode(servopin, pigpio.OUTPUT)
pi.set_servo_pulsewidth(servopin,1500)
while True:
   desiredPosition=input("where goes the servo? 0-180 ")
   if desiredPosition<0:
      break
   elif desiredPosition>180:
      desiredPosition=180
   else:
      pulseWidth = 1000 + desiredPosition*1000/180
      pi.set_servo_pulsewidth(servopin,pulseWidth)
pi.set_servo_pulsewidth(servopin,0)
pi.stop()
