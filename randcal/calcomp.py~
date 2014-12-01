#!/usr/bin/env python

import argparse
import sys
import math


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
#getcmdline()
#getdata()
#getcpow()
#getpaz()
###############################################################################

#Semi fixed stuff
nfft = 4096*8
noverlap = 2048*4

def getcmdline():
#This function gets the command line values to parse
	parser = argparse.ArgumentParser(description='Code to compare a calibration to the response')

#Here is the type of sensor we have
	parser.add_argument('-s','--sensor', type = str, action = "store", dest="sensorType", \
		default = '', help="Type of Sensor", required = False)

#Here is the period we want to normalize at
	parser.add_argument('-np','--normPeriod',type = float, action = "store", dest="normPeriod", \
		default = 10, help="Period to Normalize Calibrations", required = False)

#Here we get metadata RESP
	parser.add_argument('-mdResp','--metaDataResp', type = str, action = "store", dest="respFile", \
		default = '', help="Location of Response file", required = False)

#Allows for verbose output
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

	return parserval

def getdata(dataloc,starttime,endtime):
#A function to read in the data and trim it down
	if debug:
		print 'Data location: ' + dataloc
		print 'start time: ' + str(starttime)
		print 'end time: ' + str(endtime)
	try:
		data = read(dataloc,starttime=starttime,endtime=endtime)
		if debug:
			print 'First part of data read done'
		data.merge()
		data = data[0]
	except:
		print 'Unable to read in the data'
		sys.exit(0)
	return data

def getcpow(data1,data2):
#This function computes the cross-power
	try:
		cpow, fre = matplotlib.mlab.csd(data1.data,data2.data, NFFT=nfft, \
		noverlap = noverlap, Fs = data1.stats.sampling_rate)
		cpow = cpow[1:]
		fre = fre[1:]
	except:
		print 'Unable to compute power spectra'
		sys.exit(0)	
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


def getRespFromModel(pazModel,nfft,delta,norm):
#This function returns the response without normalization
	resp = pazToFreqResp(pazModel['poles'],pazModel['zeros'],1, \
		tracein.stats.delta, nfft, freq=False)
	resp = resp[1:]
	return resp



def getMetaDataResp(respFileLoc,norm,nfft,delta):
#This function returns the metadata response as normalized
	resp=0
	phase=0
	return resp,phase

def getbestfitresp():
#This function returns the best-fit response as normalized


	return resp




def getCalResp(fre,pIn,pOut,pInpOut,cap,norm):
#This function returns the response from the calibration
	if cap:
		resp = 10*numpy.log10((((2*math.pi*fre)**2)* (pOut/pIn)).real)
		phase = numpy.unwrap(numpy.angle((2*math.pi*fre)* pInpOut/pin))*180/math.pi
	else:
		resp = 10*numpy.log10((pOut/pIn).real)
		phase = numpy.unwrap(numpy.angle(pInpOut))*180/math.pi

#Normalize the resp and phase
	resp = resp - resp[norm]
	phase = phase - phase[norm]
	return resp,phase


def respToFAP(resp,norm):
#This function returns the phase in degrees and the amp in dB
#Convert the amplitude response to dB
	respAmp = 20*numpy.log10(abs(resp))
	respAmp = respAmp - respAmp[norm]

#Convert the phase response to degrees
	respPhase = numpy.unwrap(numpy.angle(resp))*180/math.pi
	respPhase = respPhase - respPhase[norm]

	return respAmp, respPhase



#Here is where we start the program

#Run the command line parser
parserval = getcmdline()

#User input variables
debug = parserval.debug

#Here are the start and end times
stime = UTCDateTime(parserval.stime)
etime = stime + parserval.duration


#Read in the data
tracein = getdata(parserval.inputData,stime,etime)
traceout = getdata(parserval.outputData,stime,etime)

#Lets compute the power spectra
pinpout, fre = getcpow(tracein,traceout)
pout, fre = getcpow(traceout, traceout)
pin, fre = getcpow(tracein, tracein)


period = 1/fre
#Lets find the normalization index
indexNormPeriod = numpy.argmin(numpy.abs(period - parserval.normPeriod))

#Check if the cal is resistive or not
respCal, phaseCal = getCalResp(fre,pin,pout,pinpout,parserval.capCal,indexNormPeriod)

if parserval.respFile:
	respMetaData,phaseMetaData = getMetaDataResp(parserval.respFile,tracein.stats.delta,nfft,indexNormPeriod)


#Get the response of the sensor
if parserval.sensorType:
	sensorType = parserval.sensorType
	if debug:
		print 'We are using a sensor of type: ' + sensorType
	pazresp = getpaz(sensorType)

#Now lets convert this to a FAP listing
	tfresp = getRespFromModel(pazresp,nfft,tracein.stats.delta,indexNormPeriod)
	tfamp,tfPhase = respToFAP(tfresp,indexNormPeriod)


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
p1=plt.semilogx(period,respCal,'b',label='Calibration')
if parserval.sensorType:
	p2=plt.semilogx(period,tfamp,'k',label='Nominal')
plt.xlim(1.2*min(period),max(period))
plt.ylim(-5,5)
plt.ylabel('Amplitude (dB)')
plt.legend(prop={'size':12})
plt.subplot(212)
p2=plt.semilogx(period,phaseCal,'b',label='Calibration')
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





