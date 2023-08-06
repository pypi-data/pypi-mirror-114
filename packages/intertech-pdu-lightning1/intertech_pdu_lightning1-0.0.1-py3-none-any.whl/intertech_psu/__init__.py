#!/bin/python3

import requests
import xmltodict
import time

class pdu():

    def __init__(self, host="", user="", password="") -> None:
        self._host = host
        self._user = user
        self._password = password

        self.temperature = 0
        self.humidity = 0
        self.current = 0
        self.status = "normal"
        self.outlet0 = False
        self.outlet1 = False
        self.outlet2 = False
        self.outlet3 = False
        self.outlet4 = False
        self.outlet5 = False
        self.outlet6 = False
        self.outlet7 = False

    def _update(self):
        r = requests.get('http://' + self._host + '/status.xml')
        p = xmltodict.parse(r.content)['response']
        self.temperature = p['tempBan']
        self.humidity = p['humBan']
        self.current = p['cur0']
        self.status = p['statBan']
        self.outlet0 = p['outletStat0'] == 'on'
        self.outlet1 = p['outletStat1'] == 'on'
        self.outlet2 = p['outletStat2'] == 'on'
        self.outlet3 = p['outletStat3'] == 'on'
        self.outlet4 = p['outletStat4'] == 'on'
        self.outlet5 = p['outletStat5'] == 'on'
        self.outlet6 = p['outletStat6'] == 'on'
        self.outlet7 = p['outletStat7'] == 'on'
    
    def setOutlet(self, number=1,on=True):
        if number < 1 or number > 8:
            return False
        else:
            op = '0' if on else '1'
            r = requests.get('http://' + self._host + '/control_outlet.htm?outlet' + str(number - 1) + '=1&op=' + str(op), auth=(self._user, self._password))

    def getTemperature(self):
        return self.temperature

    def getHumidity(self):
        return self.humidity

    def getCurrent(self):
        return self.current

    def getStatus(self):
        return self.status

    def getOutlet(self, number=1):
        if number == 1:
            return self.outlet0
        elif number == 2:
            return self.outlet1
        elif number == 3:
            return self.outlet2
        elif number == 4:
            return self.outlet3
        elif number == 5:
            return self.outlet4
        elif number == 6:
            return self.outlet5
        elif number == 7:
            return self.outlet6
        else:
            return False
