#!/usr/bin/python

from bluepy import btle
import struct
import time
import BB8_driver
import sys
bb8 = BB8_driver.Sphero()
bb8.connect()

bb8.start()
bb8.join()

print "RGB ..."
time.sleep(.2)
bb8.set_rgb_led(255,0,0,0,False)
time.sleep(.2)
bb8.set_rgb_led(0,255,0,0,False)
time.sleep(.2)
bb8.set_rgb_led(0,0,255,0,False)

if True:
    print "Activating User Hack Mode"
    bb8.bt.cmd(0x02, 0x42, [0x01])
else:
    print "Activating Normal Mode"
    bb8.bt.cmd(0x02, 0x42, [0x00])

bb8.bt.waitForNotifications(1.0)
print "---"

print "Reading Device Mode"
bb8.bt.cmd(0x02, 0x44)
bb8.bt.waitForNotifications(1.0)

print len("* Notification: 16 ffff000102")*" " + "^^-- 01 = User Hack Mode, 00 = Normal Mode"

print "---"
time.sleep(5)
bb8.disconnect()
