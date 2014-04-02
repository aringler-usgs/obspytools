#!/usr/bin/env python


import sys
import math
from obspy.core import read, Stream, UTCDateTime

#Debug flag
debug = bool(1)


def choptocommon(stream):
#A function to chop the data to a common time window
	stimes = []
	etimes = []

	for trace in stream:
		stimes.append(trace.stats.starttime)
		etimes.append(trace.stats.endtime)
	newstime = stimes[0]
	newetime = etimes[0]

	for curstime in stimes:
		if debug:
			print(curstime)
		if curstime >= newstime:
			newstime = curstime

	for curetime in etimes:
		if debug:		
			print(curetime)
		if curetime <= newetime:
			newetime = curetime

	if debug:
		print(newstime)
		print(newetime)
		print(stream)
	for trace in stream:	
		trace.trim(starttime=newstime,endtime=newetime)
	if debug:
		print(stream)
	return stream

def rotate(data1, data2, angle):
	theta_r = math.radians(angle)
        # create new trace objects with same info as previous
        rotatedN = data1.copy()
        rotatedE = data2.copy()
        # assign rotated data
        rotatedN.data = data1.data*math.cos(theta_r) + data2.data*math.sin(theta_r)
        rotatedE.data = data2.data*math.cos(theta_r) - data1.data*math.sin(theta_r)
        # return new streams object with rotated traces
        streams = Stream()
        streams=Stream(traces=[rotatedN, rotatedE])
       
        return streams

if debug == bool(1):
	print 'Number of arguments ' + str(len(sys.argv))

#Get command line arguments
if len(sys.argv) != 4:
	print 'Purpose: Rotate mseed file'
	print 'Usage: Angle mseed1 mseed2'
	sys.exit(0)

#Read in miniseed data
try:
	datain1 = read(sys.argv[2])
	datain1 += read(sys.argv[3])
except:
	print "Trouble reading mseed data"
	sys.exit(0)

datain = choptocommon(datain1)
datain1 = datain[0]
datain2 = datain[1]

newdata = rotate(datain1,datain2,float(sys.argv[1]))

newdata[0].write(sys.argv[2] + '.R', format = "MSEED", encoding = 5, reclen = 512)
newdata[1].write(sys.argv[3] + '.R', format = "MSEED", encoding = 5,reclen = 512)










