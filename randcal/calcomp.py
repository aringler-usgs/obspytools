#!/usr/bin/env python

import argparse
import sys
import math
import argparse

import numpy
import matplotlib.mlab
import matplotlib.pyplot as plt

from obspy.core import UTCDateTime, read, Stream
from obspy.signal import pazToFreqResp

###############################################################################
#Code to do simple calibration analysis
#By Adam Ringler
#This code takes the input and output from a random calibration and calculates
#the response
#
#Here are the current methods
#getdata()
#getcpow()
#getpaz()
###############################################################################

#Semi fixed stuff
nfft = 4096*8
noverlap = 2048*4

parser = argparse.ArgumentParser(description='Code to compare a calibration to the response')

parser.add_argument('-s','--sensor', type = str, action = "store", dest="sensorType", \
	default = '', help="Type of Sensor", required = False)

parser.add_argument('-np','--normPeriod',type = float, action = "store", dest="normPeriod", \
	default = 10, help="Period to Normalize Calibrations", required = False)

parser.add_argument('-v','--verbose',action = "store_true", dest = "debug", \
	default = False, help="Run in verbose mode")

parser.add_argument('-cIn','--calIn',type = str, action = "store", dest="inputData", \
	default = '', help="Calibration input channel data", required = True)

parser.add_argument('-cOut','--calOut',type = str, action = "store", dest = "outputData", \
	default = '', help="Calibration output channel data", required = True)

parser.add_argument('-cc','--capacitive',action = "store_true", dest = "capCal", \
	default = False, help="Allows for a capacitive calibration")

parser.add_argument('-st','--starttime',type = str, action = "store", dest = "stime", \
	default = '', help="Start time of calibration: YYYY-MM-DDTHH:MM:SS.S", required = True)

parser.add_argument('-d','--duration', type = int, action = "store", dest = "duration", \
	default = 0, help="Duration of cal in seconds", required = True)



parserval = parser.parse_args()

#User input variables
debug = parserval.debug
#stime = UTCDateTime("2013-03-13T19:37:00.0")
#duration = 4*60*60



stime = UTCDateTime(parserval.stime)
etime = stime + parserval.duration

def getdata(dataloc,starttime,endtime):
#A function to read in the data and trim it down
	if debug:
		print 'Data location: ' + dataloc
		print 'start time: ' + str(starttime)
		print 'end time: ' + str(endtime)
	data = read(dataloc,starttime=starttime,endtime=endtime)
	if debug:
		print 'First part of data read done'
	data.merge()
	data = data[0]
	
	return data

def getcpow(data1,data2):
#This function computes the cross-power
	cpow, fre = matplotlib.mlab.csd(data1.data,data2.data, NFFT=nfft, \
	noverlap = noverlap, Fs = data1.stats.sampling_rate)
	cpow = cpow[1:]
	fre = fre[1:]
	return cpow, fre

def getpaz(sensor):
#Function to get the poles and zeros
#Input the sensor type
#Output is a paz object
	debugpaz = False
	if debugpaz:
		print 'Sensor type: ' + sensor
	if sensor == 'T-120':
		paz = {'gain': 8.318710*10**17, 'zeros': [0 + 0j, 0 + 0j, -31.63 + 0j, 
			-160.0 + 0j, -350.0 + 0j, -3177.0 + 0j], 'poles':[-0.036614 + 0.037059j,  
			-0.036614 - 0.037059j, -32.55 + 0j, -142.0 + 0j, -364.0  + 404.0j, 
			-364.0 - 404.0j, -1260.0 + 0j, -4900.0 + 5204.0j, -4900.0 - 5204.0j, 
			-7100.0 + 1700.0j, -7100.0 - 1700.0j], 'sensitivity': 2.017500*10**9}
	elif sensor == 'STS-2HG':
		paz = {'gain': 5.96806*10**7, 'zeros': [0, 0], 'poles': [-0.035647 - 0.036879j,  
			-0.035647 + 0.036879j, -251.33, -131.04 - 467.29j, -131.04 + 467.29j],
			'sensitivity': 3.355500*10**10}
	elif sensor == 'STS-4B':
		paz = {'gain': 5.96806*10**7, 'zeros': [0, 0], 'poles': [-0.035647 - 0.036879j,  
			-0.035647 + 0.036879j, -251.33, -131.04 - 467.29j, -131.04 + 467.29j],
			'sensitivity': 2.5166*10**9}
	elif sensor == 'CMG-3T':
		paz = {'gain': 5.71508*10**8, 'zeros': [0, 0], 'poles': [-0.037008 - 0.037008j,  
			-0.037008 + 0.037008j, -502.65, -1005.0, -1131.0],
			'sensitivity': 3.3554*10**10}
	elif sensor == 'KS-54000':
		paz = {'gain': 86298.5, 'zeros': [0, 0], 'poles': [-59.4313,  
			-22.7121 + 27.1065j, -22.7121 + 27.1065j, -0.0048004, -0.073199],
			'sensitivity': 3.3554*10**9}
	elif sensor == '151-120':
		paz = {'gain': 60828500, 'zeros': [0, 0, -18.18], 'poles': [-772.03,  
			-20.9581, -180.3310 + 189.922j, -180.3310 - 189.922j, 
			-0.0370184 + 0.0370296j, -0.0370184 - 0.0370296j],
			'sensitivity': 2.0*10**3}
	else:
		paz={'gain': 1, 'zeros': [1 + 0j], 'poles': [1 + 0j], 'sensitivity': 1}
	
	if debugpaz:
		print(paz)
	return paz




#Here is where we start the program



try:
#Read in the data
	tracein = getdata(parserval.inputData,stime,etime)
	traceout = getdata(parserval.outputData,stime,etime)
	
except:
	print 'Can not read mSeed data'
	sys.exit(0)

try:
	pinpout, fre = getcpow(tracein,traceout)
	pout, fre = getcpow(traceout, traceout)
	pin, fre = getcpow(tracein, tracein)
except:
	print 'Can not compute the spectra'
	sys.exit(0)

period = 1/fre
#Lets find the normalization index
indexNormPeriod = numpy.argmin(numpy.abs(period - parserval.normPeriod))

#Check if the cal is resistive or not
if parserval.capCal:
	resp = 10*numpy.log10((((2*math.pi*fre)**2)* pout/pin).real)
	phase = numpy.unwrap(numpy.angle((2*math.pi*fre)* pinpout))*180/math.pi
else:
	resp = 10*numpy.log10((pout/pin).real)
	phase = numpy.unwrap(numpy.angle(pinpout))*180/math.pi

#Normalize the resp and phase
resp = resp - resp[indexNormPeriod]
phase = phase - phase[indexNormPeriod]

#Get the response of the sensor
if parserval.sensorType:
	sensorType = parserval.sensorType
	if debug:
		print 'We are using a sensor of type: ' + sensorType
	pazresp = getpaz(sensorType)

#Now lets convert this to a FAP listing
	tfpaz= pazToFreqResp(pazresp['poles'],pazresp['zeros'],1, \
		tracein.stats.delta, nfft, freq=False)
	tfpaz = tfpaz[1:]

#Convert the amplitude response to dB
	tfamp = 20*numpy.log10(abs(tfpaz))
	tfamp = tfamp - tfamp[indexNormPeriod]

#Convert the phase response to degrees
	tfPhase = numpy.unwrap(numpy.angle(tfpaz))*180/math.pi
	tfPhase = tfPhase -tfPhase[indexNormPeriod]

else:
	if debug:
		print 'No sensor type found'
	sensorType = ''


#Create a string for the title
titleString = traceout.stats.network + ' ' + traceout.stats.station + ' ' + \
	traceout.stats.location + ' ' + traceout.stats.channel + ' ' + \
	sensorType + ' ' + str(stime.year) + ' ' + str(stime.julday).zfill(3)

#Plot the results
plt.figure()
plt.subplot(211)
plt.title(titleString,fontsize=12)
p1=plt.semilogx(period,resp,'b',label='Calibration')
if parserval.sensorType:
	p2=plt.semilogx(period,tfamp,'k',label='Nominal')
plt.xlim(1.2*min(period),max(period))
plt.ylabel('Amplitude (dB)')
plt.legend(prop={'size':12})
plt.subplot(212)
p2=plt.semilogx(period,phase,'b',label='Calibration')
if parserval.sensorType:
	p3=plt.semilogx(period,tfPhase,'k',label='Nominal')
plt.xlim(1.2*min(period),max(period))
plt.ylim(-180,180)
plt.xlabel('Time (s)')
plt.ylabel('Phase (deg)')
plt.legend(prop={'size':12})
plt.savefig(traceout.stats.network + traceout.stats.station + traceout.stats.location + \
	traceout.stats.channel + str(stime.year) + str(stime.julday).zfill(3) +  \
	'.jpg', format = 'jpeg', dpi=400)





