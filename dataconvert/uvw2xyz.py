#!/usr/bin/env python
import sys
from math import sqrt
from obspy.core import read, Stream, UTCDateTime

###################################################################################################
#Code for converting from uvw to xyz mode
#By Adam Ringler
#
#choptocommon()
#rotate()
#
###################################################################################################



#Debug flag
debug = True


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

def rotate(data1, data2, data3, sen):
        # create new trace objects with same info as previous
        rotatedZ = data1.copy()
        rotatedN = data2.copy()
	rotatedE = data3.copy()
        # assign rotated data
	if sen == 'T':
        	rotatedE.data = (1/sqrt(6))*(data1.data*2 - data2.data - data3.data)
        	rotatedN.data = (1/sqrt(6))*(sqrt(3)*data2.data - sqrt(3)*data3.data)
		rotatedZ.data = (1/sqrt(3))*(data1.data + data2.data + data3.data)
	elif sen == 'S':
	        rotatedE.data = (1/sqrt(6))*(-data1.data*2 + data2.data + data3.data)
        	rotatedN.data = (1/sqrt(6))*(sqrt(3)*data2.data - sqrt(3)*data3.data)
		rotatedZ.data = (1/sqrt(6))*(data1.data + data2.data + data3.data)
	else:
		print 'Unknown sensor type'
		sys.exit(0)
	# return new streams object with rotated traces
        streams = Stream()
        streams=Stream(traces=[rotatedZ, rotatedN, rotatedE])
	if debug:
		print(streams)
       
        return streams

if debug == bool(1):
	print 'Number of arguments ' + str(len(sys.argv))

#Get command line arguments
if len(sys.argv) != 5:
	print 'Purpose: Rotate mseed file'
	print 'Usage: mseedU mseedV mseedW Sen'
	print 'Sen=S for Streckeisen Sen=T for Trillium' 
	sys.exit(0)

#Read in miniseed data
try:
	datain1 = read(sys.argv[1])
	datain1 += read(sys.argv[2])
	datain1 += read(sys.argv[3])

except:
	print "Trouble reading mseed data"
	sys.exit(0)

datain = choptocommon(datain1)
datain1 = datain[0]
datain2 = datain[1]
datain3 = datain[2]

newdata = rotate(datain1,datain2,datain3,sys.argv[4])

newdata[0].write(sys.argv[1] + '.R', format = "MSEED", encoding = 5, reclen = 512)
newdata[1].write(sys.argv[2] + '.R', format = "MSEED", encoding = 5,reclen = 512)
newdata[2].write(sys.argv[3] + '.R', format = "MSEED", encoding = 5,reclen = 512)









