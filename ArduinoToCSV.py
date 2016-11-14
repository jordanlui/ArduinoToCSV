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
from os.path import exists

# Useful variables
arduinotiming = 0.01 # Clock on arduino sketch, in seconds

# Make serial connection
serial = serial.Serial("COM5", 9600, timeout=0)

# Important functions

def WriteToCSV(datalist):
	""" This function accepts data and writes to CSV file. 
	A better optimization on this CSV script for the future would be for the CSV write to recognize the JSON hierarchy and 
	write the CSV according to JSON structure.
	"""

	global csv_success
	# Define header
	header = ["sensor","time","data1","data2"]

	# Define our file
	filename = str(time.strftime("%y_%m_%d_") + "log.csv")

	# Handling to open our file if it exists or create new one
	if exists(filename):
		# try: 
		f = csv.writer(open(filename,"a"))
			# break
		# except:
	else:
		f = csv.writer(open(filename,"a+"))
		# Write our header line out if this is a new file
		f.writerow(header)
		# for element in header:
		# 	f.write(element + ",")
		# f.write("\n")

	for row in datalist:
		f.writerow([j['sensor'],j['time'],j['data'][0],j['data'][1]])

	# for element in datalist:
	# 	if type(element)==str:
	# 		f.write(element + ",")
	# 	if type(element)==list:
	# 		for i in element:
	# 			f.write(i + ",")
	# Now we have processed all the data. Write a new line and close out.
	# f.write("\n")
	# f.close()
	csv_success = True


# Run the loop until it crashes
while True:
# for i in range(0,10):
	data = serial.readline().strip('\n\r')
	# data = serial.readline().strip('\n\r')
 
	if len(data) > 0: # We only continue if we retrieve a line of data
		
		# print 'length of data is',len(data)
		# Next we should determine if we receive a complete line of data.
		# Method one: Verify that string starts and ends with {}
		# Method two: verify a specific line length if we know what we're expecting. This option is worse if decimal points are changing in our data
	 	# print 'String begin and ends with',data[0],data[-1]
	 	
 		if data[0] == '{' and data[-1] == '}': 
 			print "String fully received"
 			j = json.loads(data)
 			print 'length of data is',len(data),' and length of JSON is ',len(j)
 			print 'entire string',j
 			print 'sensor type', j['sensor']
 			print 'time is ', j['time']
 			print 'data is 1 is',j['data'][0]
 			print 'data is 2 is',j['data'][1]

 			print 'now we write to CSV'
 			
 			WriteToCSV(j)
 			print csv_success
 			print '\n'

 			# WriteToCSV(j['sensor'])
 			# WriteToCSV(str(j['time']))
 			# WriteToCSV(str(j['data']))
 			# WriteToCSV(str(j['data']))

			 	
	 	# print len(data)
	 	# j = json.loads(data)
	 	# print(data)

	 	
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