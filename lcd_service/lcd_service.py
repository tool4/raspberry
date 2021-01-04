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

BACKLIGHT_PIN = 12
log_to_file = 1

#PWM @ 1000 Hz
GPIO.setmode(GPIO.BCM)
GPIO.setup(BACKLIGHT_PIN, GPIO.OUT)
D2A = GPIO.PWM(BACKLIGHT_PIN, 1000)
D2A.start(50)
timeout = 2

def clamp(minvalue, value, maxvalue):
    return max(minvalue, min(value, maxvalue))

lcd.write_string("Starting...")
file = open("log_lcd.txt","w", buffering=1)

try:
    while True:
        data, address = sock.recvfrom(4096)
        if(log_to_file == 1):
            print("received: %s\n" % data)
            file.write("received: %s\n" % data)
        if data:
            mode = data[:6]
            msg = data[6:]
            print(mode, msg)
            if(mode == "LIGHT:"):
                lit = int(data[6:9])
                clamp(0, lit, 100)
                D2A.ChangeDutyCycle(lit)
                lcd.cursor_pos = (1, 0)
                lcd_msg = ("BACKLIGHT: " + data[6:9] + " %" + 16 * " ")[:16]
                lcd.write_string(lcd_msg)
                timeout = 3
            else:
                if(mode == "TIME: "):
                    lcd.cursor_pos = (0, 0)
                else:
                    lcd.cursor_pos = (1, 0)
                    timeout = 3
                lcd_msg = (msg + 16 * " ")[:16]
                lcd.write_string(lcd_msg)
                lcd.cursor_pos = (1, 0)
                if(timeout > 0):
                    timeout -= 1
                else:
                    lcd.cursor_pos = (1, 3)
                    lcd.write_string((10 * "-")[:10])
                lcd.cursor_pos = (1, 0)


finally:
    print("ERROR\n")
    lcd.write_string("ERROR")
    file.write("ERROR\n")
    file.close()
