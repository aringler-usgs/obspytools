selfnoise
========

A simple utility to estimate self-noise using the Sleeman method.


Usage
========

usage: selfnoise.py [-h] [-s1 SENSORTYPE1] [-s2 SENSORTYPE2] [-s3 SENSORTYPE3]
                    [-v] -d1 DATA1 [DATA1 ...] -d2 DATA2 [DATA2 ...] -d3 DATA3
                    [DATA3 ...] [-len LEN] [-overlap OVERLAP] [-minper MINPER]
                    [-maxper MAXPER]

Program to make self-noise plots

optional arguments:
  -h, --help            show this help message and exit
  -s1 SENSORTYPE1, --sensor1 SENSORTYPE1
                        Type of Sensor possible sensors include: STS-1 M2166
                        151-120 KS-54000 STS-4B CMG-3T STS-2HG T-120 TC-Reftek
  -s2 SENSORTYPE2, --sensor2 SENSORTYPE2
                        Type of Sensor possible sensors include: STS-1 M2166
                        151-120 KS-54000 STS-4B CMG-3T STS-2HG T-120 TC-Reftek
  -s3 SENSORTYPE3, --sensor3 SENSORTYPE3
                        Type of Sensor possible sensors include: STS-1 M2166
                        151-120 KS-54000 STS-4B CMG-3T STS-2HG T-120 TC-Reftek
  -v, --verbose         Run in verbose mode
  -d1 DATA1 [DATA1 ...], --data1 DATA1 [DATA1 ...]
                        Data for PDF
  -d2 DATA2 [DATA2 ...], --data2 DATA2 [DATA2 ...]
                        Data for PDF
  -d3 DATA3 [DATA3 ...], --data3 DATA3 [DATA3 ...]
                        Data for PDF
  -len LEN              Length of PSD window in seconds default=20000 s
  -overlap OVERLAP      Overlap of windows default=0.5
  -minper MINPER        Lower period limit default=0.01 s
  -maxper MAXPER        Upper period limit default=1000.0 s


Output
========

The output is a self-noise plot along with a time series plot


Example
========

There has been an example included for some borehole test data

./selfnoise.py -d1 example/TST2BH0.seed -d2 example/TST4BH0.seed -d3 example/TST3BH0.seed -s1 T-120PH -s2 T-120PH -s3 T-120PH
/usr/lib64/python2.6/site-packages/matplotlib/backends/backend_gtk.py:621: DeprecationWarning: Use the new widget gtk.Tooltip
  self.tooltips = gtk.Tooltips()
/usr/lib64/python2.6/site-packages/matplotlib/backends/backend_gtk.py:621: DeprecationWarning: Use the new widget gtk.Tooltip
  self.tooltips = gtk.Tooltips()



To Do
========
Add additional instrument types.

Do extra error checking.
