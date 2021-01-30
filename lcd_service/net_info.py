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

def GetINTC():
    intc_price = -1.0
    try:
        url = 'https://www.marketwatch.com/investing/stock/intc'
        page = urllib.request.urlopen(url)
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
    try:
        url = 'https://forecast.weather.gov/MapClick.php?textField1=38.68&textField2=-121.16'
        page = urllib.request.urlopen(url)
        html = page.read()
        for line in html.splitlines():
            line2 = str(line)
            m2 = REGEX2.match(line2)
            if m2:
                tempf = float(m2.group("temp"))
                m3 = REGEX3.match(line2)
                if m3:
                    sky = m3.group("conditions")
    finally:
        pass
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
        print("refreshing data")
        weather = GetWeather()
        LogData("INTC.txt", GetINTC())
        LogData("IPIX.txt", GetIPIX())
        LogData("temp_mather.txt", weather[0])
        LogData("sky_mather.txt", weather[1])
        counter = counter + 1
        time.sleep(60)

finally:
    pass
