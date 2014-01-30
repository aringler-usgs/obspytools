#!/usr/bin/env python

import os

###############################################################################
#Testing script for calibration code
#By Adam Ringler
#This is simple testing code for calibrations
#
###############################################################################
os.system('./calcomp.py -cIn BC0.mseed -cOut BHZ.mseed -st 2013-03-13T19:37:00.0 -d 14400 -s KS-54000 -cc')
