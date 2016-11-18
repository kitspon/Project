#!/usr/bin/python
from bluepy import btle
import struct
import time
import BB8_driver
import sys
bb8 = BB8_driver.Sphero()
bb8.connect()
def main():
    print('Left = Turn Left')
    print('Right = Turn Right')
    print('Sleep = Sphero will sleep')
    print('Front = Forward')
    print('Back = Go back')
    while True:
        order = input("I'm Sphero Plz Order me: ")
        if order == 'Front':
	    bb8.roll(100,0,1,False)
        if order == 'Back':
            bb8.roll(100,180,1,False)
 
        if order == 'Left':
            bb8.roll(100,270,1,False)
        if order == 'Right':
            bb8.roll(100,90,1,False)
        if order == 'Disconnect':
            bb8.disconnect()
            break   
main()
