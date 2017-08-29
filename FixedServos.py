#Define class with GPIO instructions for driving

def servoLeft():
    servoPin = 16 # Servo signaling pin
    pwm = gpio.PWM(servoPin,50)
    pwm.start(1) # Makes the servo point left
    time.sleep(1)   # The time for the servo to turn left
    pwm.stop()      # Stop the servo
    
def servoStraight():
    servoPin = 16 # Servo signaling pin
    pwm = gpio.PWM(servoPin,50)
    pwm.start(6.5) # Makes the servo point straight forward
    time.sleep(1)   # The time for the servo to point forward
    pwm.stop()      # Stop the servo

def servoRight():
    servoPin = 16 # Servo signaling pin
    pwm = gpio.PWM(servoPin,50)
    pwm.start(13) # Makes the servo point right
    time.sleep(1)   # The time for the servo to turn right
    pwm.stop()      # Stop the servo
