#!/usr/bin/env python
import argparse
import sys
import math
import pickle
import numpy

from obspy.core import UTCDateTime, read, Stream
from obspy.signal import pazToFreqResp, PPSD

###############################################################################
#Code to make a PDF using input data
#By Adam Ringler
#This code takes data along with an instrument type and makes a PDF
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
			-7100.0 + 1700.0j, -7100.0 - 1700.0j], 'sensitivity': 2.017500*10**9}
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

#Start up the parser
parser = argparse.ArgumentParser(description='Program to make PDF plot')

parser.add_argument('-s','--sensor', type = str, action = "store", dest="sensorType", \
	default = '', help="Type of Sensor  possible sensors include: " + "STS-1 " + "M2166 " + \
	"151-120 " + "KS-54000 " + "STS-4B " + "CMG-3T " + "STS-2HG " + "T-120 " + "TC-Reftek " \
	, required = False)

parser.add_argument('-v','--verbose',action = "store_true", dest = "debug", \
	default = False, help="Run in verbose mode")

parser.add_argument('-d','--data',type = str, nargs='+', action = "store", dest = "data", \
	default = '', help="Data for PDF", required = True)

parser.add_argument('-len', type = int, action = "store", default=3600, help="Length of PSD window default=0.5", \
	required=False, dest = "len")

parser.add_argument('-overlap', type = float, action = "store", default=0.5, help="Overlap default=0.5", \
	required=False, dest = "overlap")

parser.add_argument('-minper', type = float, action = "store", default=0.01, help="Lower period limit default=0.01", \
	required=False, dest = "minper")

parser.add_argument('-maxper', type = float, action = "store", default=1000.0, help="Upper period limit default=1000.0", \
	required=False, dest = "maxper")

parserval = parser.parse_args()

if parserval.debug:
	debug = True
else:
	debug = False

#Get the response
if debug:
	print 'Here is the sensor:' + parserval.sensorType
pazval = getpaz(parserval.sensorType)

#Read in the data
try:	
	st = Stream()
	for dataString in parserval.data:
		if debug:
			print 'Reading in the data trace:' + dataString
		st += read(dataString)

	st.merge()
except:
	'Unable to read the data'
	sys.exit()

#Make the PDF
ppsd = PPSD(st[0].stats,paz=pazval,ppsd_length=parserval.len,overlap=parserval.overlap)
for tr in st:
	ppsd.add(tr)
try:
	if debug:
		print 'Saving the PDF'
	ppsd.plot(show_percentiles=True,percentiles=[50], filename="PDF" + \
		st[0].stats.station + st[0].stats.channel + str(st[0].stats.starttime.year)+ \
		str(st[0].stats.starttime.julday).zfill(3) + ".jpg",
		show = True, show_histogram=True, grid= False, show_coverage=False, \
		period_lim=(parserval.minper,parserval.maxper))
	per,perval = ppsd.get_percentile(percentile=50,hist_cum=None)
	perFile = open("MEDIAN" + \
		st[0].stats.station + st[0].stats.channel + str(st[0].stats.starttime.year)+ \
		str(st[0].stats.starttime.julday).zfill(3), 'w')
	for index, val in enumerate(per):
		perFile.write(str("%.2f" % val) + ',' + str(perval[index]) + '\n')
	perFile.close()
	 
		
except:
	'No PPSD saved'

		
