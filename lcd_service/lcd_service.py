from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

import socket
import sys

# Create a TCP/IP datagram socket:
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10001)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16,
    rows=2,
    pin_rs=26,
    pin_e=19,
    pins_data=[13, 6, 5, 11],
    compat_mode = True)

lcd.write_string("Waiting...")
file = open("log_lcd.txt","w", buffering=1)

while True:
    data, address = sock.recvfrom(4096)
    file.write("received: %s\n" % data)
    if data:
        mode = data[:4]
        data = data[6:]
        #print(mode)
        data = (data + 16 * " ")[:16]
        lcd.cursor_pos = (0, 0)
        lcd.write_string(data)
        #lcd.cursor_pos = (1, 0)
        #lcd.write_string(substr_c)

