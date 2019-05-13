#!/usr/bin/python

import socket
import sys
import os

ir_socket_address = "/var/run/lirc/lircd"
lcd_server_address = ('localhost', 10001)

# Create a TCP socket
ir_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Create a UDP socket
lcd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


print >>sys.stderr, 'connecting to %s' % ir_socket_address
try:
    ir_sock.connect(ir_socket_address)

except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)

try:
    print("listening to: ", ir_socket_address)
    while 1:
        data = ir_sock.recv(64)
        list = data.split()
        if( (data) ):
            print( list[1], list[2],list[3], list[0])
            sent = lcd_sock.sendto("IR:   " + list[2] + " " + list[1], lcd_server_address)
            if( list[2] == "exit" ):
                print("REBOOT!")
                os.system("pwd")
                os.system("ls")
                os.system("reboot")

finally:
    print >>sys.stderr, 'closing sockets'
    ir_sock.close()
    lcd_sock.close()
