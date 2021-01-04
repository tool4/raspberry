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

backlight = 80
step = 5

print >>sys.stderr, 'connecting to %s' % ir_socket_address
try:
    ir_sock.connect(ir_socket_address)

except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)

try:
    file = open("log_ir.txt","w", buffering=1)
    print("listening to: ", ir_socket_address)
    while 1:
        data = ir_sock.recv(64)
        list = data.split()
        if( (data) ):
            print( list[1], list[2],list[3], list[0])
            if (list[2] == "exit"):
                print("REBOOT!")
                os.system("pwd")
                os.system("ls")
                os.system("reboot")
            elif (list[2] == "up"):
                print("light up")
                if(backlight < 100):
                    backlight += step
                message = "LIGHT:" + str(backlight)
                print('sending "%s"\n' % message)
                file.write('sending "%s"\n' % message)
                sent = lcd_sock.sendto(message, lcd_server_address)
            elif (list[2] == "down"):
                print("light down")
                if(backlight > 0):
                    backlight -= step
                message = "LIGHT:" + str(backlight)
                print('sending "%s"\n' % message)
                file.write('sending "%s"\n' % message)
                sent = lcd_sock.sendto(message, lcd_server_address)
            elif (list[2] == "rotate"):
                print("restart lcd")
                os.system("systemctl restart lcd.service")
            else:
                sent = lcd_sock.sendto("IR:   " + list[2] + " " + list[1], lcd_server_address)

finally:
    print >>sys.stderr, 'closing sockets'
    ir_sock.close()
    lcd_sock.close()

