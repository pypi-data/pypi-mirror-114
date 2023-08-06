#!/bin/python3

from __init__ import pdu
import time

print("start")
a = pdu(host='pdu-felix', user='admin', password='admin')
a._update()
print("Current: " + a.getCurrent())
print("Temperature: " + a.getTemperature() + "°C")
for i in range(1,8):
    print("Outlet status " + str(i) + ": " + str(a.getOutlet(number=i)))
a.setOutlet(number=2,on=False)
time.sleep(10)
a._update()
for i in range(1,8):
    print("Outlet status " + str(i) + ": " + str(a.getOutlet(number=i)))
a.setOutlet(number=2,on=True)
time.sleep(10)
a._update()
for i in range(1,8):
    print("Outlet status " + str(i) + ": " + str(a.getOutlet(number=i)))
print("end")
