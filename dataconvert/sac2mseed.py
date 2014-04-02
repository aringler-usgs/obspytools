#!/usr/bin/env python
import sys
from obspy.core import read, Stream, UTCDateTime

###################################################################################################
#This is just a command line version of the obspy read and write
#By Adam Ringler
#
#
###################################################################################################


#Get command line arguments
if len(sys.argv) != 1:
	print 'Purpose: Convert Sac to mseed'
	print 'Usage: sacfile'
	sys.exit(0)


try:
	datain = read(sys.argv[1])

except:
	print "Trouble reading mseed data"
	sys.exit(0)


datain[0].write(sys.argv[1] + '.mseed', format = "MSEED", encoding = 5, reclen = 512)
