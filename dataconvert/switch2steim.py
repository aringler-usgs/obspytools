#!/usr/bin/env python
import sys
from obspy.core import read
import numpy


#Get command line arguments
if len(sys.argv) < 3:
	print 'Purpose: Miniseed scale change'
	print 'Usage: mseedfile ScaleFactor'
	sys.exit(0)


mseedfiles = sys.argv[1:][0]
scalefactor = float(sys.argv[2:][0])


st = read(mseedfiles)


for tr in st:
	tr.data = tr.data*scalefactor
	tr.data=tr.data.astype(numpy.int32)
	tr.stats.mseed['encoding'] = 4

st.write(mseedfiles + "SCALED",format="MSEED")
