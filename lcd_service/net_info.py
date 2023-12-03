import urllib.request
import sys
import re
import os, os.path
from os import path
import fnmatch
import sys
import time
import datetime

#<meta name="price" content="$58.67" />
regex1 = r'.*<meta name=\"price\" content=\"\$(?P<price>.*)\"\s+/>'
REGEX1 = re.compile(regex1)

#<p class="myforecast-current-lrg">39&deg;F</p>
regex2 = r'.*<p class="myforecast-current-lrg">(?P<temp>.*)&deg;F</p>'
REGEX2 = re.compile(regex2)

#<p class="myforecast-current">Clear</p>
regex3 = r'.*<p class="myforecast-current">(?P<conditions>.*)</p>'
REGEX3 = re.compile(regex3)

#def LOG():

LOG_DIR = "/var/www/html/data"

def initDir(root_dir, log_dir):
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
        print("mkdir " + log_dir)
    if not os.path.isfile(log_dir + "/index.php"):
        os.symlink(root_dir + "/../index2.php", log_dir + "/index.php")
        print("ln -s " + root_dir + "/../index.php" + " " + log_dir + "/index.php" )
    if not os.path.isfile(log_dir + "/readcsv.php"):
        os.symlink(root_dir + "/../readcsv.php", log_dir + "/readcsv.php")
        print("ln -s " + root_dir + "/../readcsv.php" + " " + log_dir + "/readcsv.php" )

def initializeLogFile(root_dir, log_name):
    YEAR = x.strftime("%Y")
    MONTH = x.strftime("%m_%B")
    DAY = x.strftime("%Y_%m_%d_%A")
    log_dir = root_dir + "/" + log_name
    initDir(root_dir, log_dir)
    log_dir = log_dir + "/" + YEAR
    initDir(root_dir, log_dir)
    log_dir = log_dir + "/" + MONTH
    initDir(root_dir, log_dir)
    csv_filename = log_dir + "/" + log_name +"_" + DAY + ".csv"
    return csv_filename

def GetINTC():
    intc_price = -1.0
    try:
        url = 'https://www.marketwatch.com/investing/stock/intc'
        page = urllib.request.urlopen(url, timeout=2)
        html = page.read()
        for line in html.splitlines():
            line2 = str(line)
            m = REGEX1.match(line2)
            if m:
                intc_price = float(m.group("price"))
    finally:
        pass
    return intc_price

    
def GetIPIX():
    ipix_price = -1.0
    try:
        url = 'https://www.marketwatch.com/investing/stock/ipix'
        page = urllib.request.urlopen(url)
        html = page.read()
        for line in html.splitlines():
            line2 = str(line)
            m = REGEX1.match(line2)
            if m:
                ipix_price = float(m.group("price"))
    finally:
        pass
    return ipix_price

def GetWeather():
    tempf = -999.0
    sky = "unknown"
    print("get weather...")
    try:
        url = 'https://forecast.weather.gov/MapClick.php?textField1=38.68&textField2=-121.16'
        page = urllib.request.urlopen(url)
        html = page.read()
        for line in html.splitlines():
            line2 = str(line)
            print(line)
            m2 = REGEX2.match(line2)
            if m2:
                tempf = float(m2.group("temp"))
                m3 = REGEX3.match(line2)
                if m3:
                    sky = m3.group("conditions")
    except:
        print("exception")
    finally:
        pass
    print("get weather returned: %.2f, %s" %(tempf, sky))
    return [tempf, sky]


def SendMessage(message):
    x = datetime.datetime.now()
    timestamp = x.strftime("%d %b  %H:%M:%S")
    data = message.encode('ascii')
    print(timestamp + ": sending: " + message)
    file.write('%s sending "%s"\n' %(timestamp, message))
    sent = sock.sendto(data, server_address)


def LogData(filename, data):
    print(str(data))
    f = open("files/" + filename, "w")
    f.write(str(data) + "\n")
    f.close()


counter = 0
try:
    while True:
        force = False
        if len(sys.argv) > 1:
            if sys.argv[1] == "-f":
                force = True
        x = datetime.datetime.now()
        timestamp = x.strftime("%H:%M")
        hour = int(x.strftime("%H"))
        minute = int(x.strftime("%M"))
        minutes = hour * 60 + minute
        day = int(x.strftime("%w"))
        #stock market is open Mon-Fri between 6:30 and 13:30 PST:
        if not counter == 0 and not(day > 0 and day < 6 and minutes >= 5 * 60 + 20 and minutes <= 14 * 60 + 30) and not force:
            print(timestamp + " market closed, sleeping for 10 min\n")
            time.sleep(600)
            continue

        print("refreshing data")
        weather = [0.0, 'unknown'] #GetWeather()
        intc = GetINTC()
        print("intc: %.2f" %(intc))
        ipix = GetIPIX()
        temp = weather[0]
        conditions = weather[1]
        LogData("INTC.txt", intc)
        LogData("IPIX.txt", ipix)
        LogData("temp_mather.txt", temp)
        LogData("sky_mather.txt", conditions)

        x = datetime.datetime.now()
        timestamp = x.strftime("%H:%M")
        csv_filename = initializeLogFile(LOG_DIR, "netinfo")
        if not os.path.exists(csv_filename):
            f = open(csv_filename, "w")
            f.write("timestamp, intc, ipix, temp_mather, conditions\n")
            f.close()
        f = open(csv_filename, "a")
        f.write("%s, %5.2f, %5.2f, %.2f, %s\n"
                %(timestamp, intc, ipix, temp, conditions))
        f.close()
        print("%s, %5.2f, %5.2f, %.2f, %s\n"
                %(timestamp, intc, ipix, temp, conditions))
        counter = counter + 1
        time.sleep(120) #2 min

#except:
#    print("ERROR")
finally:
    print("END")
    pass
