#-------------------Accelerometer-------------------------------
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

#------------------------servo movement--------------------
while 1:
    try:
        message, address = s.recvfrom(8192)
        
        var = message.split()
        temp2 = str(var[3].strip())
        temp3 = re.sub('[^0-9.-]', '', temp2)
        
        print (temp3)


        if (float(temp3) > 0.3):
            print ("Rotate right")
        elif (float(temp3) < -0.3):
            print ("Rotate left")
        else:
            print ("Straight forward")
        
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
#----------------------END servo movement--------------------
