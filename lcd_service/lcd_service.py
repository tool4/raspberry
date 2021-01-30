import sys
import time
import datetime
import board
import digitalio

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

BACKLIGHT_PIN = 12
log_to_file = 1

#PWM @ 1000 Hz
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(BACKLIGHT_PIN, GPIO.OUT)
#D2A = GPIO.PWM(BACKLIGHT_PIN, 1000)
#D2A.start(50)

timeout = 2
marker = 0
temp_in = ""

def clamp(minvalue, value, maxvalue):
    return max(minvalue, min(value, maxvalue))

marker_chars = ['-', '\\', '|', '/', '-', '\\', '|', '/' ]

#lcd.write_string("Starting...")
file = open("log_lcd.txt","w", buffering=1)
flip = 0
counter = 0
line = "Not set yet"
timestamp = "00-00 00:00:00"

try:
    while True:
        #lcd.cursor_pos = (0, 15)
        #marker = (marker + 1) % len(marker_chars)
        #% len(marker_chars)
        #character = marker_chars[marker]
        #if marker == 1 or marker == 5:
        #    lcd.write_string(unichr(1))
        #else:
        #    lcd.write_string(character)

        x = datetime.datetime.now()
        timestamp = x.strftime("%d-%m %H:%M:%S") + 16 * " "
        line = 16 * ' '
        if counter == 0:
            #temp C
            f = open("files/data_temp_c.txt", "r")
            temp_c = f.readline().strip()
            f.close()
            line =  "Temp: %4.1f F" %(float(temp_c))
        elif counter == 1:
            f = open("files/data_temp_f.txt", "r")
            temp_f = f.readline().strip()
            f.close()
            line =  "Temp: %4.1f F" %(float(temp_f))
        elif counter == 2:
            f = open("files/INTC.txt", "r")
            intc = f.readline().strip()
            f.close()
            line =  "INTC: %.02f $" %(float(intc))
        elif counter == 3:
            f = open("files/IPIX.txt", "r")
            ipix = f.readline().strip()
            f.close()
            line =  "IPIX: %.02f $" %(float(ipix))
        elif counter == 4:
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
        counter = (counter + 1) % 5
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
