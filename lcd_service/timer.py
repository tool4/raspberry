import socket
import sys
import time
import datetime

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10001)
message = 'This is the message.  It will be repeated.'

try:
    file = open("log_timer.txt","w", buffering=1)
    while True:
        x = datetime.datetime.now()
        message = "TIME: " + x.strftime("%d %b  %H:%M:%S")
        file.write('sending "%s"\n' % message)
        sent = sock.sendto(message, server_address)
        time.sleep(1)

finally:
    if (file):
        file.write("closing socket\n")
        file.close()
    sock.close()
