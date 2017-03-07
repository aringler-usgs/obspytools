#!/usr/bin/env python

import argparse
import sys

from obspy.core.event import read_events
from obspy.core import UTCDateTime

###############################################################################
#Code to replace eq_info
#By Adam Ringler
#This is a quick piece of python code to replace the old eq_info in
#FORTRAN it uses USGS webservices to obtain the events and then parses 
#everything out
#
###############################################################################

#Here are the fixed variables
website = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'

#Lets setup the command line parser
parser = argparse.ArgumentParser(description='Code to get earthquake info')

#Here are the number of days
parser.add_argument('-n','--number', action = "store",dest = "number", \
default = 1, help="Number of days to search", type = int, required = False)

#Start date of the search
parser.add_argument('-t','--time',type = str, action = "store", dest= "time", \
default = "", required = True, help="Start time to search from: YYYY,DDD")

#To be run in verbose mode
parser.add_argument('-v','--verbose',action = "store_true",dest="debug", \
default = False, help="Run in verbose (debug) mode")

#Here is the minimum magnitude to search over
parser.add_argument('-mM','--minMag',action="store",dest = "minMag", \
default = 2.5, help= "Minimum magnitude", type = float, required = False)

#Here is the maximum magnitude to search over
parser.add_argument('-MM','--MaxMag',action="store",dest = "maxMag", \
default = 9.9, help= "Minimum magnitude", type = float, required = False)

#We probably want to search over depth also
parser.add_argument('-md','--mindep',action="store",dest = "minDep", \
default = 0.0, help= "Minimum depth (km)", type = float, required = False)


parserval = parser.parse_args()

if parserval.debug:
        print 'Running in debug mode'
        debug = True
else:
        debug = False


#Lets set the search for the following magnitude scale
searchParameter = '&minmagnitude=' + str(parserval.minMag) + \
	'&maxmagnitude=' + str(parserval.maxMag) + \
	'&mindepth=' + str(parserval.minDep) + \
	'&eventtype=earthquake'

#Lets setup the time for the search
if parserval.time:
        try:
		if debug:
			print 'Here is the time in: ' + \
				parserval.time.split(',')[0]

                stime = UTCDateTime(parserval.time.split(',')[0] + "-" + \
                        parserval.time.split(',')[1] + "T00:00:00.0") 
        except:
                print 'Problem reading epoch'
                sys.exit(0)

        if debug:
                print 'Here is the epoch time of interest:' + str(stime)   

	etime = stime + parserval.number*24*60*60 

#Lets format for the USGS webservices
stimeString = 'starttime=' + (stime.formatIRISWebService()).replace('T','%20')
etimeString = 'endtime=' + (etime.formatIRISWebService()).replace('T','%20')

if debug:
	print 'Start time string: ' + stimeString
	print 'End time string: ' + etimeString

#Here is the final query
querystring = website + stimeString + '&' + etimeString + searchParameter

#Lets read it in a quakeML format
cat = read_events(querystring)

#Now lets scan through and print out the results
for event in cat:
#Just use one magnitude
	magString = str(event.magnitudes[0].mag)

#Lets use all the different origins we find
	for origin in event.origins:

#Format the time for year doy hr:mn:sc
		timeString = str(origin.time.year) + ' ' + \
			str(origin.time.julday).zfill(3) + \
			' ' + str(origin.time.hour).zfill(2) + ':' + \
			str(origin.time.minute).zfill(2) + ':' + \
			str(origin.time.second).zfill(2)

#Lets only get a few sig figs for everything else		  
		latString = ("%4.2f" % origin.latitude).rjust(6)
		lonString = ("%4.2f" % origin.longitude).rjust(7)
		depthString = ("%4.2f" % (origin.depth/1000)).rjust(6)
#Print the event to the screen
		print timeString + ' ' + latString + ' ' + lonString + ' ' + \
			depthString + ' ' + magString
