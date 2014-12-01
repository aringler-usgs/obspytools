calcomp.py
==========


Usage
==========

./calcomp.py -h
usage: calcomp.py [-h] [-s SENSORTYPE] [-np NORMPERIOD] [-mdResp RESPFILE]
                  [-v] -cIn INPUTDATA -cOut OUTPUTDATA [-cc] -st STIME -d
                  DURATION

Code to compare a calibration to the response

optional arguments:
  -h, --help            show this help message and exit
  -s SENSORTYPE, --sensor SENSORTYPE
                        Type of Sensor
  -np NORMPERIOD, --normPeriod NORMPERIOD
                        Period to Normalize Calibrations
  -mdResp RESPFILE, --metaDataResp RESPFILE
                        Location of Response file
  -v, --verbose         Run in verbose mode
  -cIn INPUTDATA, --calIn INPUTDATA
                        Calibration input channel data
  -cOut OUTPUTDATA, --calOut OUTPUTDATA
                        Calibration output channel data
  -cc, --capacitive     Allows for a capacitive calibration
  -st STIME, --starttime STIME
                        Start time of calibration: YYYY-MM-DDTHH:MM:SS.S
  -d DURATION, --duration DURATION

