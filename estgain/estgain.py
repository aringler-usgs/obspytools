#!/usr/bin/env python
import argparse
import sys
import math
import pickle
import numpy

from obspy.core import UTCDateTime, read, Stream
from obspy.signal import pazToFreqResp

from matplotlib.mlab import csd
from math import pi


###############################################################################
#Code to do a simple gain estimate for two sensors
#By Adam Ringler
#This code takes data along with a sensitivity to estimate the sensitivity of
#another instrument.
#
###############################################################################

def cp(tr1,tr2,lenfft,lenol,delta):
    sr = 1/delta
    cpval,fre = csd(tr1.data,tr2.data,NFFT=lenfft,Fs=sr,noverlap=int(lenol*lenfft),scale_by_freq=True)
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
    parser = argparse.ArgumentParser(description='Program to estimate gain ratio')

    parser.add_argument('-s','--sensitivity', type = int, action = "store", dest="sensorType1", \
        default = 2000, help="Sensitivity of sensor 1 in V/m/s", required = False)

    parser.add_argument('-v','--verbose',action = "store_true", dest = "debug", \
        default = False, help="Run in verbose mode")

    parser.add_argument('-d1','--data1',type = str, nargs='+', action = "store", dest = "data1", \
        default = '', help="Reference data for Gain", required = True)

    parser.add_argument('-d2','--data2',type = str, nargs='+', action = "store", dest = "data2", \
        default = '', help="Test data for Gain", required = True)

    parser.add_argument('-len', type = int, action = "store", default=20000, \
        help="Length of PSD window in seconds default=20000 s", \
        required=False, dest = "len")

    parser.add_argument('-overlap', type = float, action = "store", default=0.5, \
        help="Overlap of windows default=0.5", \
        required=False, dest = "overlap")

    parser.add_argument('-minper', type = float, action = "store", default=4.0, \
        help="Lower period limit default=4.0 s", \
        required=False, dest = "minper")

    parser.add_argument('-maxper', type = float, action = "store", default=8.0, \
        help="Upper period limit default=8.0 s", \
        required=False, dest = "maxper")

    parserval = parser.parse_args()
    return parserval


if __name__ == '__main__':

    #Get the parservalues
    parserval = getargs()

    if parserval.debug:
        debug = True
    else:
        debug = False



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

    except:
        'Unable to read the data'
        sys.exit()

    if debug:
        for tr in st:
            print 'Here is the data stream: ' + str(tr)    
        print 'Here is the window length of your PSDs: ' + str(parserval.len)
        print 'Here is the overlap: ' + str(parserval.overlap)


    st = choptocommon(st)
    delta1 = st[0].stats.delta
    delta2 = st[1].stats.delta

    try:
        inst1resp = (parserval.sensorType1)**2
        inst2resp = 1.


        (p11, fre1) = cp(st[0],st[0],parserval.len,parserval.overlap,delta1)
        (p22, fre2) = cp(st[1],st[1],parserval.len,parserval.overlap,delta2)
        p11 = p11/inst1resp
        p22 = p22/inst2resp

    except:
        print 'Unable to compute the spectra'
        sys.exit()

    per1 = 1/fre1
    per2 = 1/fre2
    mask1 = (per1 < parserval.maxper) & (parserval.minper < per1)
    mask2 = (per2 < parserval.maxper) & (parserval.minper < per2)
    if debug:
        print(numpy.real(p11[mask1]))
        print(numpy.real(p22[mask2]))

    diffs = numpy.average(numpy.real(p11[mask1]))/numpy.average(numpy.real(p22[mask2]))
    sigma = numpy.std((numpy.real(p22[mask1])/numpy.real(p11[mask2]))**.5)
    print 'Sensitivity of instrument 2: ' + str(1/(diffs**.5)) + '+/-' + str(2.5*sigma) + str(' V/m/s')
    print 'Sensitivity of instrument 1 (input): ' + str(parserval.sensorType1) + str(' V/m/s')
        










        
