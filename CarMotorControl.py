def driveForward(t):
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, True) # Enable RH wheels to spin forward
    gpio.output(15, True) # Enable LH wheels to spin forward
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True) # EN2 Enable LH wheels to spin
    time.sleep(t)
    
def driveBackward(t):
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, False) # Enable RH wheels to spin backwards
    gpio.output(15, False) # Enable LH wheels to spin backwards
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True) # EN2 Enable LH wheels to spin
    time.sleep(t)
    
def driveLeftForward(t):
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, True) # Enabels RH wheels to spin forward
    gpio.output(15, False) # Enabels LH wheels to spin backwards
    gpio.output(7, True)  # EN1 Enables RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    time.sleep(t)
    
def driveRightForward(t):
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, False) # Enabels RH wheels to spin backwards
    gpio.output(15, True) # Enabels LH wheels to spin forward
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, True) # EN2 Enables LH wheels to spin
    time.sleep(t)

def driveLeftBackward(t):
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, False) # Enabels RH wheels to spin backwards
    gpio.output(15, False) # Enabels LH wheels to spin backwards
    gpio.output(7, True)  # EN1 Enables RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    time.sleep(t)
  
def driveRightBackward(t):
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, False) # Enabels RH wheels to spin backwards
    gpio.output(15, False) # Enabels LH wheels to spin forward
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, True) # EN2 Enables LH wheels to spin
    time.sleep(t)

def driveLeftPivot(t):
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, True) # Enable LH wheels to spin backward
    gpio.output(15, False) # Enable RH wheels to spin forward
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True) # EN2 Enable LH wheels to spin
    time.sleep(t)
    
def driveRightPivot(t):
    gpio.output(7, False)  # EN1 Disable RH wheels to spin
    gpio.output(11, False) # EN2 Disable LH wheels to spin
    gpio.output(13, False) # Enable RH wheels to spin forward
    gpio.output(15, True) # Enable LH wheels to spin backwards
    gpio.output(7, True)  # EN1 Enable RH wheels to spin
    gpio.output(11, True) # EN2 Enable LH wheels to spin
    time.sleep(t)
	
def stopAll():
    gpio.output(7, 0)
    gpio.output(11, 0)
    gpio.output(13, 0)
    gpio.output(15, 0)
	
def driveDirection(axis0, axis1, t):
    axis0 = int(round(axis0))
    axis1 = int(round(axis1))  
    if axis0 == 0 and axis1 == -1:
        driveForward(t)
        print ("Going Forward")
    if axis0 == 0 and axis1 == 1:
        driveBackward(t)
        print ("Going Backward")
    if axis0 == -1 and axis1 == 0:
        driveLeftForward(t)
        print ("Going LeftForward")
    if axis0 == 1 and axis1 == 0:
        driveRightForward(t)
        print ("Going RightForward")
    if axis0 == -1 and axis1 == 1:
        driveLeftBackward(t)
        print ("Going LeftBackward")
    if axis0 == 1 and axis1 == 1:
        driveRightBackward(t)
        print ("Going RightBackward")
    if axis0 == -1 and axis1 == 0:
        driveLeftPivot(t)
        print ("LeftPivot")
    if axis0 == 1 and axis1 == 0:
        driveRightPivot(t)
        print ("RightPivot")
    if axis0 == 0 and axis1 == 0:
        stopAll()