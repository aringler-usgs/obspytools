#!/usr/bin/env python

import sys
import glob

from obspy.core import read 

###################################################################################################
#Code for converting mseed to bdf file format
#by Adam Ringler
#
#
#
#
###################################################################################################


#Debug flag
debug = False

if debug:
	print 'Number of arguments ' + str(len(sys.argv))

#Get command line arguments
if len(sys.argv) < 2:
	print 'Purpose: Miniseed to bdf'
	print 'Usage: mseedfile'
	sys.exit(0)

#Read in miniseed data
mseedfiles = sys.argv[1:]
if debug:
	print mseedfiles

for curfile in mseedfiles:
	if debug:
		print curfile
	try:
		datain = read(curfile)
	except:
		print "Trouble reading mseed data"
		sys.exit(0)

	len(datain)

	#For each trace make a bdf file
	for trace in datain:
	#Make bdf file name
		if debug:
			print 'Writing a trace'
		filename ='DATA_' + trace.stats.network + '_' + trace.stats.station + '_' + \ 
			trace.stats.location + '_' + trace.stats.channel + '_' + \ 
			str(trace.stats.starttime.year) + '_' + \
			str(trace.stats.starttime.julday).zfill(3) + '_' + \ 
			str(trace.stats.starttime.hour).zfill(2) + '_' + \ 
			str(trace.stats.starttime.minute).zfill(2) + '.bdf'
		if debug == bool(1):
			print 'Writing to ' + filename
		filein = open(filename,'w')
		#Run through the data
		dataptindex = 0
		currtime = trace.stats.starttime
		for dataval in trace.data:
		#Every 1000 samples write a new header
			if divmod(dataptindex,1000)[1] == 0:
				filein.write('NET ' + trace.stats.network + '\n')
				filein.write('STA ' + trace.stats.station + '\n')
				filein.write('LOC ' + trace.stats.location + '\n')
				filein.write('COMP' + trace.stats.channel + '\n')
				filein.write('RATE' + str(trace.stats.sampling_rate) + '\n')
				timestamp = str(currtime.year) + ',' + \ 
					str(currtime.julday).zfill(3) + ',' + \ 
					str(currtime.hour).zfill(2) + ':' + \ 
					str(currtime.minute).zfill(2) + ':' + \
					str(currtime.second).zfill(2) + '.0' + \ 
					str(currtime.microsecond)
				filein.write('TIME' + timestamp + '\n')
				if len(trace.data) - dataptindex > 1000:
					filein.write('NSAM1000\n')
				else:
					filein.write('NSAM' + str(len(trace.data) - dataptindex) + '\n')
				filein.write('DATA\n')
				currtime += (1000 / trace.stats.sampling_rate)
				if debug == bool(1):
					print 'Current time ' + str(currtime)
			filein.write(str(dataval) + '\n')
			dataptindex += 1
		filein.close()
sys.exit(0)
