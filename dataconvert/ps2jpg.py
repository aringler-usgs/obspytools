#!/usr/bin/env python
import sys
import os

###################################################################################################
#Simple program for converting ps to jpg using gs
#by Adam Ringler
#
#
#
###################################################################################################
debug = False
#Start of the main part of the program
if not len(sys.argv) == 2:
	print "Usage: ps-file"
	exit(0)

psfile = sys.argv[1]
if debug:
	print "Here is the extension:" + psfile[-3:].strip()
if psfile[-3:] == ".ps":
	if debug:
		print "Removing the old extenion"
	jpgfile = psfile.replace('.ps','.jpg')
else:
	jpgfile = psfile + '.jpg'
cmd2run = 'gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -sOutputFile=' + jpgfile + ' -r100 ' + psfile
if debug:
	print "jpgfile:" + jpgfile
	print 'Running:' + cmd2run
os.system(cmd2run)



