import os
import socket
import re
import sys
import time
import datetime


print(socket.gethostbyname(socket.gethostname()))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.0.4', 10001)
print ('starting up on %s port %s' %(server_address))
sock.bind(server_address)

log_to_file = 1

timeout = 2
marker = 0
temp_in = ""

def clamp(minvalue, value, maxvalue):
    return max(minvalue, min(value, maxvalue))

marker_chars = ['-', '\\', '|', '/', '-', '\\', '|', '/' ]

LOG_DIR = "/var/www/html/data/weather"
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)
log_file  = open(LOG_DIR + "/log_udp.txt","w", buffering=1)
data_file = open(LOG_DIR +"/data_udp.txt","w", buffering=1)
flip = 0
counter = 0

#TEMP: 10.10C, 43.30%h, 11.41V
regex1 = r"TEMP: (?P<tempc>\S+)C, (?P<humidity>\S+)\%h, (?P<voltage>\S+)V"
REGEX1 = re.compile(regex1)


try:
    x = datetime.datetime.now()
    timestamp = x.strftime("%d %b  %H:%M:%S")
    print( "Started at: %s" %(timestamp))
    while True:
        data, address = sock.recvfrom(4096)
        #data, address = [0, 0]
        data = str(data)
        #print("got: " + data)
        m1 = REGEX1.match(data)
        if not m1:
            print("Line: [%s] not matched, skipping" %(data))
            continue
        x = datetime.datetime.now()
        timestamp = x.strftime("%d %b  %H:%M:%S")
        YEAR = x.strftime("%Y")
        MONTH = x.strftime("%m_%B")
        DAY = x.strftime("%Y_%m_%d_%A")
        LOG_DIR2 = LOG_DIR + "/" + YEAR
        if not os.path.isdir(LOG_DIR2):
            os.mkdir(LOG_DIR2)
            os.system('ln -s /var/www/html/index2.php ' + LOG_DIR2 + '/index.php')
        LOG_DIR3 = LOG_DIR2 + "/" + MONTH
        if not os.path.isdir(LOG_DIR3):
            os.mkdir(LOG_DIR3)
            os.system('ln -s /var/www/html/index2.php ' + LOG_DIR3 + '/index.php')

        csv_filename = LOG_DIR3 + "/temperature_" + DAY + ".csv"
        if not os.path.exists(csv_filename):
            f = open(csv_filename, "w")
            f.write("timestamp, temp_in_c, temp_in_f, humidity, voltage\n")
            f.close()
        
        if(log_to_file == 1):
            #print("received: %s" % data)
            log_file.write("%s: received: %s\n" %(timestamp, data))
        if data:
            mode = data[:6]
            msg = data[6:]
            #print(mode, msg)
            if(mode == "TEMP: "):
                #28.40C, 35.00%h
                temp_str = m1.group("tempc")
                humidity = m1.group("humidity")
                voltage  = float(m1.group("voltage"))
                temp_in_c = float(temp_str)
                temp_in_f = temp_in_c * 1.8 + 32.0
                f = open("files/temp_log.txt", "a")
                f.write(timestamp + ": " + msg + "\n")
                f.close()
                f = open("files/data_temp_c.txt", "w")
                f.write(str(temp_in_c) + "\n")
                f.close()
                f = open("files/data_temp_f.txt", "w")
                f.write("%5.02f\n" %(temp_in_f))
                f.close()
                f = open("files/voltage.txt", "w")
                f.write("%5.02f\n" %(voltage))
                f.close()
                print("%s: %s" %(timestamp, msg))
                timestamp = x.strftime("%H:%M:%S")
                f = open(csv_filename, "a")
                f.write("%s, %5.2f, %5.2f, %s, %s\n"
                        %(timestamp, temp_in_c, temp_in_f, str(humidity), str(voltage)))
                f.close()

finally:
    x = datetime.datetime.now()
    timestamp = x.strftime("%d %b  %H:%M:%S")
    print("ERROR at %s\n" % timestamp)
    log_file.write("ERROR at %s\n" % timestamp)
    log_file.close()
