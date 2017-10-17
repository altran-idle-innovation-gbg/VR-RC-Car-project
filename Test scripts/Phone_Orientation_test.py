# -------------------------------------------------------
import socket
import traceback
import os

socket_path = '/tmp/uv4l.socket'
try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise
s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
s.bind(socket_path)
s.listen(1)
# -------------------------------------------------------

pygame.init()
pygame.joystick.init()
try:
    joyStick = pygame.joystick.Joystick(0)
    joyStick.init()
except:
    pass
screen = pygame.display.set_mode((240, 240))
pygame.display.set_caption('VR CAR')

print 'awaiting connection...'
connection, client_address = s.accept()
print client_address
stop = True
while stop:
    data_in_string = connection.recv(256)
    print data_in_string
    if event.type == pygame.KEYDOWN:
        if event.key == 32:
            stop = False
        elif event.key == K_ESCAPE:
            stop = False
        elif event.type == pygame.QUIT:
            stop = False
connection.close()
try:
    joyStick.quit()
except:
    pass
