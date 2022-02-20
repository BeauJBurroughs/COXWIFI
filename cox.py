#!/usr/bin/python3
import requests
import string
import random
import netifaces
import os
import json
from datetime import datetime
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = {
'http':'http://127.0.0.1:8080',
'https':'http://127.0.0.1:8080'
}
s = requests.Session()

def getRandomName():
    lines = open('/usr/share/dirb/wordlists/others/names.txt').read().splitlines()
    result = random.choice(lines)
    return result
def getRandomLettersforName(length):
    letters = string.ascii_lowercase
    result = ''.join((random.choice(letters)) for x in range(length))
    return result
def getRandomDomain():
    lines = ['@gmail.com','@yahoo.com','@aol.com','@hotmail.com','@outlook.com','@live.com']
    result = random.choice(lines)
    return result

#def getRandomMacNums():
#    letters = "1234567890ABCDEF"
#    result = ''.join((random.choice(letters)) for x in range(2))
#    return result
#def generateMac():
#    MAC = getRandomMac() + ":" + getRandomMac() + ":" + getRandomMac() + ":" + getRandomMac() + ":" + getRandomMac() + ":" + getRandomMac()
#    return MAC

def getActualMac():
    IFNAME = 'wlan0'
    MAC = str(netifaces.ifaddresses(IFNAME)[netifaces.AF_LINK][0]['addr'])
    return MAC

def generateNames():
    FIRSTNAME = getRandomName()
    LASTNAME = getRandomName()
    DOMAIN = getRandomDomain()
    EMAIL = FIRSTNAME + "." + LASTNAME + DOMAIN
    return FIRSTNAME,LASTNAME,EMAIL


def firstReq():
    HEADERS = {
'Host': 'uwp-wifi-access-portal.cox.com',
'Connection': 'close',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-User': '?1',
'Sec-Fetch-Dest': 'document',
'sec-ch-ua': '\";Not A Brand\";v=\"99\", \"Chromium\";v=\"88\"',
'sec-ch-ua-mobile': '?0',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.9'
}
    URL = f'https://uwp-wifi-access-portal.cox.com/splash?mac-address={MAC}&ap-mac=BC:9B:68:0E:25:01&ssid=CoxWiFi&vlan=103&nas-id=NRFKWAGB01.at.at.cox.net&block=false&unique=$HASH'
    r1 = s.get(URL, headers=HEADERS,verify=False, allow_redirects=True) #, proxies=PROXIES)
    print (r1.cookies)
    return r1.cookies

def secondReq(cookie):
    HEADERS2 = {
'Host': 'uwp-wifi-access-portal.cox.com',
'Connection': 'close',
'sec-ch-ua': '\";Not A Brand\";v=\"99\", \"Chromium\";v=\"88\"',
'sec-ch-ua-mobile': '?0',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-User': '?1',
'Sec-Fetch-Dest': 'document',
'Referer': f'https://uwp-wifi-access-portal.cox.com/splash?mac-address={MAC}&ap-mac=BC:9B:68:0E:25:01&ssid=CoxWiFi&vlan=103&nas-id=NRFKWAGB01.at.at.cox.net&block=false&unique=$HASH',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.9'
}
    URL = 'https://uwp-wifi-access-portal.cox.com/subscribers/trial'
    r2 = s.get(URL, headers=HEADERS2, cookies=cookie, verify=False, allow_redirects=True) #, proxies=PROXIES)
    return r2.cookies

def thirdReq(cookie2,FIRSTNAME,LASTNAME,EMAIL,MAC):
    HEADERS3 = {
'Host': 'uwp-wifi-access-portal.cox.com',
'Connection': 'close',
'Content-Length': '281',
'requestType': 'submission',
'sec-ch-ua-mobile': '?0',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
'Content-Type': 'application/json',
'Accept': 'application/json, text/plain, */*',
'Caller-Name': 'UWP',
'Transaction-Id': 'UWP-xwehyx71b3',
'Conversation-Id': 'CONV-o22ere8f7tt',
'sec-ch-ua': '\";Not A Brand\";v=\"99\", \"Chromium\";v=\"88\"',
'Origin': 'https://uwp-wifi-access-portal.cox.com',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Dest': 'empty',
'Referer': 'https://uwp-wifi-access-portal.cox.com/subscribers/trial',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.9'
}

    DATA = '''{"macAddress": "''' + MAC + '''",
"ssidName": "CoxWiFi",
"nasId": "NRFKWAGB01.at.at.cox.net",
"vlan": "103",
"propertyId": 1,
"firstName": "''' + FIRSTNAME + '''",
"lastName": "''' + LASTNAME + '''",
"internetProvider": "Cox",
"emailAddress": "''' + EMAIL + '''",
"uniquePropertyId": "0010107152",
"apMacAddress": "BC:9B:68:0E:25:01"}'''
    URL = 'https://uwp-wifi-access-portal.cox.com/access/coxwifi/registerUser'
    r3 = s.post(URL, headers=HEADERS3, cookies=cookie2, data=DATA, verify=False, allow_redirects=True) #, proxies=PROXIES)
    return 'Success'

def reconnectWifi():
    os.system("nmcli d wifi connect CoxWiFi")
    time.sleep(60)
    return "Successfully reconnected"

def register():
    FIRSTNAME,LASTNAME,EMAIL = generateNames()
    cookie = firstReq()
    cookie2 = secondReq(cookie)
    thirdReq(cookie2,FIRSTNAME,LASTNAME,EMAIL,MAC)
    f = open('log.txt','a')
    f.write("Todays Date: " + str(datetime.now()) + "\n")
    f.write("New Mac: " + MAC + "\n")
    f.write("New Email: " + EMAIL + "\n")
    f.write("========================================================================")
    return True



reconnectWifi()
MAC = getActualMac()
register()
