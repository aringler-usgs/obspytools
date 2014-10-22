#!/usr/bin/env python
import sys
from obspy.core import read, Stream
import numpy
import glob
import os


#Get command line arguments
if len(sys.argv) < 3:
	print 'Purpose: Miniseed scale change'
	print 'Usage: mseedfile ScaleFactor'
	sys.exit(0)



mseedfiles = sys.argv[1:-1]





scalefactor = float(sys.argv[-1])




for mseedfile in mseedfiles:
	st = Stream()
	st += read(mseedfile)


	for tr in st:
		tr.data = tr.data*scalefactor
		tr.data=tr.data.astype(numpy.int32)
		tr.stats.mseed['encoding'] = 4


	curdir = os.getcwd()
	mseedfileabb = mseedfile.split("/")[-1]
	st.write(mseedfileabb + "SCALED",format="MSEED")
