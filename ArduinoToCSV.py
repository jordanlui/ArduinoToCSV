#!/usr/bin/python
# -*- coding: utf-8 -*-

# First basic build to read data from Arduino COM port
# We also try to write to csv now

# Initialize
import serial
import sys
import time
import csv
import json

# Useful variables
arduinotiming = 0.01 # Clock on arduino sketch, in seconds

# Make serial connection
serial = serial.Serial("COM5", 9600, timeout=0)

# Run the loop until it crashes
while True:
# for i in range(0,10):
	data = serial.readline().strip('\n\r')
	# data = serial.readline().strip('\n\r')
 
	if len(data) > 0: # We only continue if we retrieve a line of data
		
		# Next we should determine if we receive a complete line of data.
		# Method one: Verify that string starts and ends with {}
		# Method two: verify a specific line length if we know what we're expecting
	 	print 'String begin and ends with',data[0],data[-1]
	 	print 'length of data is',len(data)
 		# if data[0] == '{' and data[-1] == '}': # Fact that this doesn't work tells me that something wrong with encoding
	 	
	 	# print len(data)
	 	j = json.loads(data)
	 	print(data)
	 	
	 	# print(j)
	 	# print j['sensor']
	 	# print j['data']
 	
	time.sleep(0.1)

# json test
# data = '{"sensor":"gps","time":1351824120,"data":[48.756080,2.302038]}'
# if data[0] == '{' and data[-1] == '}':
# 	print 'String properly formatted'
# 	j = json.loads(data)
# 	print(data)
# 	print 'sensor is',j['sensor']
# 	print 'data is', j['data'] 
# 	print json.dumps(j, indent=4) # Pretty print the data