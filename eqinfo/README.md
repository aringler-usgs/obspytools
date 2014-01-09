eqinfopy
========

Earthquake info using webservices to get quick information about events


Usage
========

The following usage is allowed:
eqinfo.py -h
usage: eqinfo.py [-h] [-n NUMBER] -t TIME [-v] [-mM MINMAG] [-MM MAXMAG]
                 [-md MINDEP]

Code to get earthquake info

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        Number of days to search
  -t TIME, --time TIME  Start time to search from: YYYY,DDD
  -v, --verbose         Run in verbose (debug) mode
  -mM MINMAG, --minMag MINMAG
                        Minimum magnitude
  -MM MAXMAG, --MaxMag MAXMAG
                        Minimum magnitude
  -md MINDEP, --mindep MINDEP
                        Minimum depth (km)


Output
========

The output is in rows with the year, day of year, hour, minute, second,
latitude, longitude, depth, and magnitude


To Do
========
We need to add different event types beyond earthquakes.

We also need to add various possible outputs.

This could potentially be used for finding arrival times also.
