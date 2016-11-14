#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This function will read the data from Arduino and write to CSV.
"""

# Initialize
import serial
import sys
import time
import csv
import json
from os.path import exists

# Useful variables
arduinotiming = 0.01 # Clock on arduino sketch, in seconds

print 'starting our script'
# Make serial connection
serial = serial.Serial("COM5", 9600, timeout=0)
print 'connected to Serial Device'

# Important functions

def WriteToCSV(datalist):
	""" This function accepts data and writes to CSV file. 
	A better optimization on this CSV script for the future would be for the CSV write to recognize the JSON hierarchy and 
	write the CSV according to JSON structure.
	"""

	global csv_success
	# Define header
	header = ["pot","fsr1","fsr2","fsr3","omron8","omron8","omron8","omron8","omron8","omron8","omron8","omron8","omron16","omron16","omron16","omron16","omron16","omron16","omron16","omron16","omron16","omron16","omron16","omron16","omron16","omron16","omron16","omron16"]

	# Define our file
	filename = str(time.strftime("%y_%m_%d_") + "log.csv")

	# Handling to open our file if it exists or create new one
	if exists(filename):
		# try: 
		f = csv.writer(open(filename,"a"),lineterminator='\n')
			# break
		# except:
	else:
		f = csv.writer(open(filename,"a+"),lineterminator='\n')
		# Write our header line out if this is a new file
		f.writerow(header)
		


	# For datum in datalist: # This isn't needed if I spell out my assignments below
	# Better method would involve something where the data is in a single hierarchy and then written piecewise
		
	f.writerow([datalist['pot'],datalist['fsr1'],datalist['fsr2'],datalist['fsr3'],
		datalist['omron8'][0],datalist['omron8'][1],datalist['omron8'][2],datalist['omron8'][3],datalist['omron8'][4],datalist['omron8'][5],datalist['omron8'][6],datalist['omron8'][7],
		datalist['omron16'][0],datalist['omron16'][1],datalist['omron16'][2],datalist['omron16'][3],datalist['omron16'][4],datalist['omron16'][5],datalist['omron16'][6],datalist['omron16'][7],datalist['omron16'][8],datalist['omron16'][9],datalist['omron16'][10],datalist['omron16'][11],datalist['omron16'][12],datalist['omron16'][13],datalist['omron16'][14],datalist['omron16'][15]])

	
	csv_success = True


# Run the loop until it crashes
while True:
# for i in range(0,10):
	print 'reading data'
	data = serial.readline().strip('\n\r')
	# data = serial.readline().strip('\n\r')
 
	if len(data) > 0: # We only continue if we retrieve a line of data
		
		# print 'length of data is',len(data)
		# Next we should determine if we receive a complete line of data.
		# Method one: Verify that string starts and ends with {}
		# Method two: verify a specific line length if we know what we're expecting. This option is worse if decimal points are changing in our data
	 	# print 'String begin and ends with',data[0],data[-1]
	 	# print 'data length',len(data)

	 # 	test1 = '{"pot":525,"omron8":[21,21,21,21,21,21,21,21],"omron16":[20,20,20,20,20,20,20,20,20,20,20,20,22,22,22,19],"fsr1":0,"fsr2":0,"fsr3":0}'
		# test2 = json.loads(test1)
		# print 'testdata in json format',test2
		# data = test1
		
		print len(data)

 		if data[0] == '{' and data[-1] == '}': 
 			print "String fully received"
 			j = json.loads(data)
 			print 'length of data is',len(data),' and length of JSON is ',len(j)
 			print 'entire string',j
 			print json.dumps(j, indent=4) # pretty print the data
 			print 'data from FSRs',j['fsr1'],j['fsr2'],j['fsr3']

 			print 'now we write to CSV'
 			
 			WriteToCSV(j)
 			if csv_success == True:
				print 'Written to CSV'
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
 	
	time.sleep(0.3)

# json test
# data = '{"sensor":"gps","time":1351824120,"data":[48.756080,2.302038]}'
# if data[0] == '{' and data[-1] == '}':
# 	print 'String properly formatted'
# 	j = json.loads(data)
# 	print(data)
# 	print 'sensor is',j['sensor']
# 	print 'data is', j['data'] 
# 	print json.dumps(j, indent=4) # Pretty print the data