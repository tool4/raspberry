import sys
import time
import datetime
import board
import digitalio
import Adafruit_DHT

#from lirc import RawConnection
#conn = RawConnection()
#def GetIrCode():
#    global conn
#    try:
#        keypress = conn.readline(.0001)
#    except:
#        keypress=""
#    if (keypress != "" and keypress != None):
#        data = keypress.split()
#        sequence = data[1]
#        command = data[2]
#        return command
#    return '00'

# Backlight PWM:
from gpiozero import PWMLED
from time import sleep
led = PWMLED(12)
led.value = 0.7

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D11)
lcd_d6 = digitalio.DigitalInOut(board.D5)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d4 = digitalio.DigitalInOut(board.D13)
lcd_columns = 16
lcd_rows = 2

import adafruit_character_lcd.character_lcd as characterlcd
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

log_to_file = 1
timeout = 2
marker = 0
temp_in = ""

def clamp(minvalue, value, maxvalue):
    return max(minvalue, min(value, maxvalue))

marker_chars = ['-', '\\', '|', '/', '-', '\\', '|', '/' ]

#lcd.write_string("Starting...")
file = open("log_lcd.txt","w", buffering=1)
flip = 0
mode = 0
real_counter = 0
line = "Not set yet"
timestamp = "00-00 00:00:00"
NUM_STATES = 1
unit = 'C'

try:
    while True:
        ircode = '00'#GetIrCode()
        if ircode != '00':
            print(ircode)
            if ircode == 'CD_TRACK+':
                mode += 1
            if ircode == 'CD_TRACK-':
                mode -= 1
            ircode = '00'
            print("mode: %s" %mode)
        if (real_counter % 10) == 0:
            humidity1, temperature1 = Adafruit_DHT.read_retry(22, 21)
            humidity2, temperature2 = Adafruit_DHT.read_retry(22, 16)
            humidity3, temperature3 = Adafruit_DHT.read_retry(22, 20)
            #temperature, unit = (9/5) * temperature + 32, 'F'
        x = datetime.datetime.now()
        timestamp = x.strftime("%d-%m %H:%M:%S") + 16 * " "
        line = 16 * ' '
        if mode == 0:
            if (real_counter % 9) < 3:
                humidity, temperature = humidity1, temperature1
                line = 'T1=%.1f%s H1=%.1f' %(temperature, unit, humidity)
            elif (real_counter % 9) < 6:
                humidity, temperature = humidity2, temperature2
                line = 'T2=%.1f%s H2=%.1f' %(temperature, unit, humidity)
            else:
                humidity, temperature = humidity3, temperature3
                line = 'T3=%.1f%s H3=%.1f' %(temperature, unit, humidity)
        elif mode == 1:
            #temp C
            f = open("files/data_temp_c.txt", "r")
            temp_c = f.readline().strip()
            f.close()
            line =  "Temp: %4.1f C" %(float(temp_c))
        elif mode == 2:
            f = open("files/data_temp_f.txt", "r")
            temp_f = f.readline().strip()
            f.close()
            line =  "Temp: %4.1f F" %(float(temp_f))
        elif mode == 3:
            f = open("files/INTC.txt", "r")
            intc = f.readline().strip()
            f.close()
            line =  "INTC: %.02f $" %(float(intc))
        elif mode == 4:
            f = open("files/IPIX.txt", "r")
            ipix = f.readline().strip()
            f.close()
            line =  "IPIX: %.02f $" %(float(ipix))
        elif mode == 5:
            f = open("files/voltage.txt", "r")
            volt = f.readline().strip()
            f.close()
            line =  "Voltage: %.02f V" %(float(volt))
        line = line + 16 * " "
        timestamp = timestamp[:15] + '\n'
        str = timestamp[:16] + line[:16]
        lcd.message =  str
        print("%s: %s" %(timestamp.strip(), line.strip()))
        time.sleep(1.0)
#        counter = (counter + 1) % NUM_STATES
        real_counter += 1
except KeyboardInterrupt:
    print("Closed by user\n")
    lcd.message = "Closed by user"
    file.write("%s - Closed by user\n" %(timestamp))
    file.close()
except:
    print("ERROR on line: [%s]\n" %(line))
    lcd.message = "ERROR on:\n" + line
    file.write("ERROR on line: [%s]\n" %(line))
    file.close()
finally:
    pass
