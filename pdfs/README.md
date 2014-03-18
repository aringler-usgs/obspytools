mkpdf
========

A simple utility to make a PDF plot


Usage
========

usage: mkpdf.py [-h] [-s SENSORTYPE] [-v] -d DATA [DATA ...] [-len LEN]
                [-overlap OVERLAP] [-minper MINPER] [-maxper MAXPER]

Program to make PDF plot

optional arguments:
  -h, --help            show this help message and exit
  -s SENSORTYPE, --sensor SENSORTYPE
                        Type of Sensor possible sensors include: STS-1 M2166
                        151-120 KS-54000 STS-4B CMG-3T STS-2HG T-120 TC-Reftek
  -v, --verbose         Run in verbose mode
  -d DATA [DATA ...], --data DATA [DATA ...]
                        Data for PDF
  -len LEN              Length of PSD window default=0.5
  -overlap OVERLAP      Overlap default=0.5
  -minper MINPER        Lower period limit default=0.01
  -maxper MAXPER        Upper period limit default=1000.0


Output
========

The output is a PDF plot for the data used

Example
========

There has been an example included for IU station TUC

./mkpdf.py -s STS-1 -d example/00_LHZ.512.seed -v
Here is the sensor:STS-1
Reading in the data trace:example/00_LHZ.512.seed
Saving the PDF


To Do
========
Add additional instrument types.

Save a pickle file upon exit.

Do extra error checking.
