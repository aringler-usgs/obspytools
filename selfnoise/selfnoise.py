#!/usr/bin/env python
import argparse
import sys
import math
import pickle
import numpy

from obspy.core import UTCDateTime, read, Stream
from obspy.signal import pazToFreqResp, PPSD
from obspy.signal.spectral_estimation import get_NLNM, get_NHNM
from matplotlib.mlab import csd
from math import pi
from matplotlib.pyplot import (figure,axes,plot,xlabel,ylabel,title,subplot,legend,savefig,show,xscale, xlim)

###############################################################################
#Code to do Sleeman self-noise
#By Adam Ringler
#This code takes data along with an instrument type and make a self-noise plot
#
#Here are the current methods
#getpaz()
###############################################################################


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
			-7100.0 + 1700.0j, -7100.0 - 1700.0j], 'sensitivity': 3.4153*10**18}
	elif sensor == 'T-120PH':
		paz = {'poles': [-0.03859+0.03649j, -0.03859-0.03649j, \
			-190, -158+193j, -158-193j, -639+1418j, -639-1418j], \
			'zeros': [0,0,-106,-158], \
			'sensitivity': 1201.0*1.695*(10**9)*(2**26)/40}
	elif sensor == 'TC-Reftek':
		paz = {'gain': 8.184*10**11, 'zeros': [0 + 0j, 0 + 0j, -434.1 + 0j],
			'poles':[-0.03691 + 0.03712j, -0.03691 - 0.03712j, -371.2 + 0j,
			-373.9  + 475.5j, -373.9 - 475.5j, -588.4 + 1508.0j, -588.4 - 1508.0j], 
			'sensitivity': 4.7143*10**8}
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
	elif sensor == 'STS-1':
		paz = {'gain': 3948.58, 'zeros': [0, 0], 'poles': [-0.01234 - 0.01234j,  
			-0.01234 + 0.01234j, -39.18 - 49.12j, -39.18 + 49.12j],
			'sensitivity': 3.3554432*10**9}
	elif sensor == 'M2166':
		paz = {'gain': 3948.58, 'zeros': [0, 0], 'poles': [-0.01234 - 0.01234j,  
			-0.01234 + 0.01234j, -39.18 - 49.12j, -39.18 + 49.12j],
			'sensitivity': 1.00663296*10**9}
	else:
		paz={'gain': 1, 'zeros': [1 + 0j], 'poles': [1 + 0j], 'sensitivity': 1}
	
	if debugpaz:
		print(paz)
	return paz

def computeresp(resp,delta,lenfft):
	respval = pazToFreqResp(resp['poles'],resp['zeros'],resp['sensitivity'],t_samp = delta, 
		nfft=lenfft,freq = False)
	respval = numpy.absolute(respval*numpy.conjugate(respval))
	respval = respval[1:]
	return respval

def cp(tr1,tr2,lenfft,lenol,delta):
	sr = 1/delta
	cpval,fre = csd(tr1.data,tr2.data,NFFT=lenfft,Fs=sr,noverlap=lenol,scale_by_freq=True)
	fre = fre[1:]
	cpval = cpval[1:]
	return cpval, fre

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




def getargs():
#Start up the parser
	parser = argparse.ArgumentParser(description='Program to make self-noise plots')

	parser.add_argument('-s1','--sensor1', type = str, action = "store", dest="sensorType1", \
		default = '', help="Type of Sensor  possible sensors include: " + "STS-1 " + "M2166 " + \
		"151-120 " + "KS-54000 " + "STS-4B " + "CMG-3T " + "STS-2HG " + "T-120 " + "TC-Reftek " \
		, required = False)

	parser.add_argument('-s2','--sensor2', type = str, action = "store", dest="sensorType2", \
		default = '', help="Type of Sensor  possible sensors include: " + "STS-1 " + "M2166 " + \
		"151-120 " + "KS-54000 " + "STS-4B " + "CMG-3T " + "STS-2HG " + "T-120 " + "TC-Reftek " \
		, required = False)

	parser.add_argument('-s3','--sensor3', type = str, action = "store", dest="sensorType3", \
		default = '', help="Type of Sensor  possible sensors include: " + "STS-1 " + "M2166 " + \
		"151-120 " + "KS-54000 " + "STS-4B " + "CMG-3T " + "STS-2HG " + "T-120 " + "TC-Reftek " \
		, required = False)

	parser.add_argument('-v','--verbose',action = "store_true", dest = "debug", \
		default = False, help="Run in verbose mode")

	parser.add_argument('-d1','--data1',type = str, nargs='+', action = "store", dest = "data1", \
		default = '', help="Data for PDF", required = True)

	parser.add_argument('-d2','--data2',type = str, nargs='+', action = "store", dest = "data2", \
		default = '', help="Data for PDF", required = True)

	parser.add_argument('-d3','--data3',type = str, nargs='+', action = "store", dest = "data3", \
		default = '', help="Data for PDF", required = True)

	parser.add_argument('-len', type = int, action = "store", default=20000, \
		help="Length of PSD window in seconds default=20000 s", \
		required=False, dest = "len")

	parser.add_argument('-overlap', type = float, action = "store", default=0.5, \
		help="Overlap of windows default=0.5", \
		required=False, dest = "overlap")

	parser.add_argument('-minper', type = float, action = "store", default=0.01, \
		help="Lower period limit default=0.01 s", \
		required=False, dest = "minper")

	parser.add_argument('-maxper', type = float, action = "store", default=1000.0, \
		help="Upper period limit default=1000.0 s", \
		required=False, dest = "maxper")

	parserval = parser.parse_args()
	return parserval


parserval = getargs()




if parserval.debug:
	debug = True
else:
	debug = False



#Get the response
if debug:
	print 'Here is the sensor 1:' + parserval.sensorType1
	print 'Here is the sensor 2:' + parserval.sensorType2
	print 'Here is the sensor 3:' + parserval.sensorType3


try:
	pazval1 = getpaz(parserval.sensorType1)
	pazval2 = getpaz(parserval.sensorType2)
	pazval3 = getpaz(parserval.sensorType3)
except:
	print 'Can not get the responses for the instruments'
	sys.exit()



#Read in the data
try:	
	st = Stream()
	for dataString in parserval.data1:
		if debug:
			print 'Reading in the data trace 1:' + dataString
		st += read(dataString)
	for dataString in parserval.data2:
		if debug:
			print 'Reading in the data trace 2:' + dataString
		st += read(dataString)
	for dataString in parserval.data3:
		if debug:
			print 'Reading in the data trace 3:' + dataString
		st += read(dataString)

	st.merge()

except:
	'Unable to read the data'
	sys.exit()

if debug:
	for tr in st:
		print 'Here is the data stream: ' + str(tr)	
	print 'Here is the window length of your PSDs: ' + str(parserval.len)
	print 'Here is the overlap: ' + str(parserval.overlap)


st = choptocommon(st)
delta = st[0].stats.delta

try:
	inst1resp = computeresp(pazval1,delta,parserval.len)
	inst2resp = computeresp(pazval2,delta,parserval.len)
	inst3resp = computeresp(pazval3,delta,parserval.len)

	(p11, fre1) = cp(st[0],st[0],parserval.len,parserval.overlap,delta)
	(p22, fre1) = cp(st[1],st[1],parserval.len,parserval.overlap,delta)
	(p33, fre1) = cp(st[2],st[2],parserval.len,parserval.overlap,delta)

	(p21, fre1) = cp(st[1],st[0],parserval.len,parserval.overlap,delta)
	(p13, fre1) = cp(st[0],st[2],parserval.len,parserval.overlap,delta)
	(p23, fre1) = cp(st[1],st[2],parserval.len,parserval.overlap,delta)


	n11 = ((2*pi*fre1)**2)*(p11 - p21*p13/p23)/inst1resp
	n22 = ((2*pi*fre1)**2)*(p22 - numpy.conjugate(p23)*p21/numpy.conjugate(p13))/inst2resp
	n33 = ((2*pi*fre1)**2)*(p33 - p23*numpy.conjugate(p13)/p21)/inst3resp
except:
	print 'Unable to compute the spectra'
	sys.exit()


NLNMper,NLNMpower = get_NLNM()
NHNMper,NHNMpower = get_NHNM()


titlelegend = 'Self-Noise: ' + str(st[0].stats.starttime.year) + ' ' + str(st[0].stats.starttime.julday) + ' ' + \
str(st[0].stats.starttime.hour) + ':' + str(st[0].stats.starttime.minute) + ':' + str(st[0].stats.starttime.second) + \
' ' + str(st[0].stats.npts*delta) + ' seconds'
noiseplot = figure(1)
subplot(1,1,1)
title(titlelegend,fontsize=12)
plot(1/fre1,10*numpy.log10(((2*pi*fre1)**2)*p11/inst1resp),'r',label='PSD ' + st[0].stats.station + ' ' + \
st[0].stats.location + ' ' + st[0].stats.channel + ' ' + parserval.sensorType1)
plot(1/fre1,10*numpy.log10(((2*pi*fre1)**2)*p22/inst2resp),'b',label='PSD ' + st[1].stats.station + ' ' + \
st[1].stats.location + ' ' + st[1].stats.channel + ' ' + parserval.sensorType2)
plot(1/fre1,10*numpy.log10(((2*pi*fre1)**2)*p33/inst3resp),'g',label='PSD ' + st[2].stats.station + ' ' + \
st[2].stats.location + ' ' + st[2].stats.channel + ' ' + parserval.sensorType3)
plot(1/fre1,10*numpy.log10(n11),'r:',label='Noise ' + st[0].stats.station + ' ' + st[0].stats.location + ' ' + \
st[0].stats.channel + ' ' + parserval.sensorType1)
plot(1/fre1,10*numpy.log10(n22),'b:',label='Noise ' + st[1].stats.station + ' ' + st[1].stats.location + ' ' + \
st[1].stats.channel + ' ' + parserval.sensorType2)
plot(1/fre1,10*numpy.log10(n33),'g:',label='Noise ' + st[2].stats.station + ' ' + st[2].stats.location + ' ' + \
st[2].stats.channel + ' ' + parserval.sensorType3)
plot(NLNMper,NLNMpower,'k')
plot(NHNMper,NHNMpower,'k')
legend(prop={'size':12})
xlabel('Period (s)')
ylabel('Power rel. 1 (m/s^2)^2/Hz')
xscale('log')
xlim((numpy.amin(1/fre1), numpy.amax(1/fre1) ))
savefig('NOISE' + str(st[0].stats.starttime.year) + str(st[0].stats.starttime.julday) + \
	str(st[0].stats.starttime.hour) + str(st[0].stats.starttime.minute) + \
st[0].stats.station + st[0].stats.location + st[0].stats.channel + \
st[1].stats.station + st[1].stats.location + st[1].stats.channel + \
st[2].stats.station + st[2].stats.location + st[2].stats.channel + \
'.jpg', format = 'jpeg', dpi=400)




titlelegend = 'Time Series: ' + str(st[0].stats.starttime.year) + ' ' + str(st[0].stats.starttime.julday) + ' ' + \
str(st[0].stats.starttime.hour) + ':' + str(st[0].stats.starttime.minute) + ':' + str(st[0].stats.starttime.second) + \
' ' + str(st[0].stats.npts*delta) + ' seconds'
tval=numpy.arange(0,st[0].stats.npts / st[0].stats.sampling_rate, st[0].stats.delta)
tseriesplot = figure(2)
title(titlelegend,fontsize=12)

subplot(311)
title(titlelegend,fontsize=12)
plot(tval,st[0].data,'r',label='TSeries ' + st[0].stats.station + ' ' + \
st[0].stats.location + ' ' + st[0].stats.channel + ' ' + parserval.sensorType1)
legend(prop={'size':12})
xlim((0, numpy.amax(tval) ))
subplot(312)
plot(tval,st[1].data,'b',label='TSeries ' + st[1].stats.station + ' ' + \
st[1].stats.location + ' ' + st[1].stats.channel + ' ' + parserval.sensorType2)
legend(prop={'size':12})
xlim((0, numpy.amax(tval) ))
subplot(313)
plot(tval,st[2].data,'g',label='TSeries ' + st[2].stats.station + ' ' + \
st[2].stats.location + ' ' + st[2].stats.channel  + ' ' + parserval.sensorType3)
xlabel('Time (s)')
ylabel('Counts')
legend(prop={'size':12})
xlim((0, numpy.amax(tval) ))
savefig('TSERIES' + str(st[0].stats.starttime.year) + str(st[0].stats.starttime.julday) + \
	str(st[0].stats.starttime.hour) + str(st[0].stats.starttime.minute) + \
st[0].stats.station + st[0].stats.location + st[0].stats.channel + \
st[1].stats.station + st[1].stats.location + st[1].stats.channel + \
st[2].stats.station + st[2].stats.location + st[2].stats.channel + \
'.jpg', format = 'jpeg', dpi=400)
















	
