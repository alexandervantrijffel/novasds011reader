#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import serial, time, struct

from serial import Serial
ser = serial.Serial()
ser.port = "/dev/ttyUSB0" # Set this to your serial port
ser.baudrate = 9600

ser.open()
ser.flushInput()

byte, lastbyte = "\x00", "\x00"

while True:
    lastbyte = byte
    byte = ser.read(size=1)
    
    # We got a valid packet header
    if lastbyte == b"\xAA" and byte == b"\xC0": 
        sentence = ser.read(size=8) # Read 8 more bytes
        readings = struct.unpack('<hhxxcc',sentence) # Decode the packet - big endian, 2 shorts for pm2.5 and pm10, 2 reserved bytes, checksum, message tail
        
        pm_25 = readings[0]/10.0
        pm_10 = readings[1]/10.0

        # ignoring the checksum and message tail
        print ("PM 2.5:",pm_25,"μg/m^3  PM 10:",pm_10,"μg/m^3")
