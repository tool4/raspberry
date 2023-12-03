#!/usr/bin/python

import socket
import sys
import os

lcd_server_address = ('192.168.1.115', 10001)
# Create a UDP socket
lcd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

from lirc import RawConnection

conn = RawConnection()

def GetIrCode():
    global conn
    try:
        keypress = conn.readline(.0001)
    except:
        keypress=""
    if (keypress != "" and keypress != None):
        data = keypress.split()
        sequence = data[1]
        command = data[2]
        return command
    return '00'

backlight = 80
step = 5

try:
    file = open("log_ir.txt","w", buffering=1)
    while 1:
        data = GetIrCode()
        if( (data != '00') ):
            print(data)
            if (data == "exit"):
                print("REBOOT!")
                os.system("pwd")
                os.system("ls")
                os.system("reboot")
            elif (data == "up"):
                print("light up")
                if(backlight < 100):
                    backlight += step
                message = "LIGHT:" + str(backlight)
                print('sending "%s"\n' % message)
                file.write('sending "%s"\n' % message)
                sent = lcd_sock.sendto(message, lcd_server_address)
            elif (data == "down"):
                print("light down")
                if(backlight > 0):
                    backlight -= step
                message = "LIGHT:" + str(backlight)
                print('sending "%s"\n' % message)
                file.write('sending "%s"\n' % message)
                sent = lcd_sock.sendto(message, lcd_server_address)
            elif (data == "CD_CLEAR"):
                print("restart lcd")
                os.system("systemctl restart lcd.service")
            #else:
            #    sent = lcd_sock.sendto("IR:   " + data, lcd_server_address)

finally:
    print('closing sockets')
    lcd_sock.close()

