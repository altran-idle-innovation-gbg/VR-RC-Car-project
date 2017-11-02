import pigpio
import time

servopin1 = 18
servopin2 = 19

pi = pigpio.pi()
pi.set_mode(servopin1, pigpio.OUTPUT)
pi.set_mode(servopin2, pigpio.OUTPUT)
pi.set_servo_pulsewidth(servopin1, 1500)
pi.set_servo_pulsewidth(servopin2, 1500)

while True:
    desiredPosition1 = input("where goes servo up/down? 0-180 ")
    desiredPosition2 = input("where goes servo Left/Right? 0-180 ")

    if desiredPosition1 < 0 or desiredPosition2 < 0:
        break
    elif desiredPosition1 > 180 or desiredPosition2 > 180:
        desiredPosition1 = 180
        desiredPosition2 = 180
    else:
        pulseWidth1 = 1000 + desiredPosition1 * 1000 / 180
        pulseWidth2 = 1000 + desiredPosition2 * 1000 / 180
        pi.set_servo_pulsewidth(servopin1, pulseWidth1)
        pi.set_servo_pulsewidth(servopin2, pulseWidth2)
pi.set_servo_pulsewidth(servopin1, 0)
pi.set_servo_pulsewidth(servopin2, 0)
pi.stop()
