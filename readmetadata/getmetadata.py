#!/usr/bin/env python 

import argparse
import sys
import time
import os.path
from obspy.core import UTCDateTime
from obspy.xseed import Parser
from time import gmtime, strftime


def getstalist(sp,epochtime):
#A function to get a station list
	stations = []
	for cursta in sp.stations:
#As we scan through blockettes we need to find blockettes 50 
		for blkt in cursta:
			if blkt.id == 50:
#Pull the station info for blockette 50
				stacall = blkt.station_call_letters.strip()
				if type(blkt.end_effective_date) is str:
					curdoy = strftime("%j",gmtime())
					curyear = strftime("%Y",gmtime())
					curtime = UTCDateTime(curyear + "-" + curdoy + "T00:00:00.0") 
					if blkt.start_effective_date <= epochtime:
						stations.append(blkt.network_code.strip() + ' ' + \
						blkt.station_call_letters.strip())
				elif blkt.start_effective_date <= epochtime and blkt.end_effective_date >= epochtime:
					stations.append(blkt.network_code.strip() + ' ' + \
					blkt.station_call_letters.strip())	
	return set(stations)

def getstalistlocation(sp,epochtime):
#A function to get a station list
	stations = []
	for cursta in sp.stations:
#As we scan through blockettes we need to find blockettes 50 
		for blkt in cursta:
			if blkt.id == 50:
#Pull the station info for blockette 50
				stacall = blkt.station_call_letters.strip()
				if type(blkt.end_effective_date) is str:
					curdoy = strftime("%j",gmtime())
					curyear = strftime("%Y",gmtime())
					curtime = UTCDateTime(curyear + "-" + curdoy + "T00:00:00.0") 
					if blkt.start_effective_date <= epochtime:
						stations.append(blkt.network_code.strip() + ' ' + \
						blkt.station_call_letters.strip() + ' ' + \
						blkt.site_name.strip())
				elif blkt.start_effective_date <= epochtime and blkt.end_effective_date >= epochtime:
					stations.append(blkt.network_code.strip() + ' ' + \
					blkt.station_call_letters.strip() + ' ' + blkt.site_name.strip())	
	return set(stations)


def getinstrument(sp,epochtime):
	instlookup = []
	instindex = []
	instruments = []
	for blkt in sp.abbreviations:
		if blkt.id == 33:
			instindex.append(blkt.abbreviation_lookup_code)
			instlookup.append(blkt.abbreviation_description)
			instindex.append(blkt.abbreviation_lookup_code)

#A function to get the instrument type
	for cursta in sp.stations:
#As we scan through blockettes we need to find blockettes 50 and 52
		for blkt in cursta:	
			if blkt.id == 50:
#Pull the station info for blockette 50
				stacall = blkt.station_call_letters.strip()
			if blkt.id == 52:
				if type(blkt.end_date) is str:
					curdoy = strftime("%j",gmtime())
					curyear = strftime("%Y",gmtime())
					curtime = UTCDateTime(curyear + "-" + curdoy + "T00:00:00.0") 
					if blkt.start_date <= epochtime:
						instruments.append(stacall + ' ' + blkt.location_identifier + ' ' + \
						instlookup[blkt.instrument_identifier - 1])
				elif blkt.start_date <= epochtime and blkt.end_date >= epochtime:
					instruments.append(stacall + ' ' + blkt.location_identifier + ' ' + \
					instlookup[blkt.instrument_identifier - 1])
	instruments = set(instruments)
	return instruments


#Set the date of interest until we add date flag default to current time
curdoy = strftime("%j",gmtime())
curyear = strftime("%Y",gmtime())



#Terminal input parser code
parser = argparse.ArgumentParser(description='Code to parse a dataless')
parser.add_argument('-s', '--station', action = "store_true",dest="station", \
help="Prints a list of stations for the date given", default = False)
parser.add_argument('-sl', '--stationlist', action = "store_true",dest="stationlist", \
help="Prints a list of station locations for the date given", default = False)
parser.add_argument('-si', '--stationinstrument', action = "store_true",dest="stationinst", \
help="Prints a list of stations and instruments for the date given", default = False)
parser.add_argument('-v', '--verbose', action = "store_true", dest="verbose", default = False)
parser.add_argument('dataless',action = "store", default = str,help="Dataless file in seed format")
parser.add_argument('-d', '--date', type = str, action = "store", dest="date", \
default = curyear + ' ' + curdoy, required=False, help="Date in YYYY DDD format")
parseresult = parser.parse_args()

#Start of program
if parseresult.verbose:
	print "Running in verbose mode"
	verbose = True
else:
	verbose = False

#Here we set the date for the epoch of interest
if verbose:
	print "Here is the date for the epoch"
	print parseresult.date
	print "Here is the year " + parseresult.date.split()[0]
	print "Here is the day " + parseresult.date.split()[1]
try:
	epochtime = UTCDateTime(parseresult.date.split()[0] + "-" + parseresult.date.split()[1] + "T00:00:00.0") 
except:
	print "Problem reading epoch time"
	sys.exit(0)


#Read in the dataless
if verbose:
	print "Reading in the dataless"
#try: 
	
sp = Parser(parseresult.dataless)
#except:
#	print "Not able to read dataless"
#	sys.exit(0)

if parseresult.station:
	if verbose:
		print "Making a station list"
	stations = getstalist(sp,epochtime)
	for sta in stations:
		print sta

if parseresult.stationlist:
	if verbose:
		print "Making a station list"
	stations = getstalistlocation(sp,epochtime)
	for sta in stations:
		print sta

if parseresult.stationinst:
	if verbose:
		print "Making a station list"
	stations = getinstrument(sp,epochtime)
	for sta in stations:
		print sta

