# Trimble BX992
Python library for Trimble BX992 GPS receiver configuration

## Introduction
Trimble GPS receiver can be configured through a serial link with binary format commands (https://www.trimble.com/OEM_ReceiverHelp)
The `gpsconf.py` Python script accepts a YAML (https://en.wikipedia.org/wiki/YAML) configuration file where each record is a set of
parameters (items) to configure. Configuration items will be encoded and sent by serial link to the receiver.

## Record and item names

### General Controls

|item name|type|constraint|description|
|-|-|-|-|
|ELEVATION MASK|byte|range [0:90]|Elevation mask in degrees|
|PDOP MASK|byte|range [0:255]|Position Dilution of Precision Mask|
|RTK POSITIONING MODE|byte|map<br/>0:synchronous<br/>1:low latency|RTK positioning mode|
|POSITIONING SOLUTION SELECTION|byte|map<br/>0:Use best available solution<br/>1:Produce DGPS and autonomous solutions<br/>2:Produce DGPS, RTK float and autonomous solutions<br/>3:Produce RTK fix, DGPS and Autonomous solutions|Controls use of DGPS and RTK solutions|
|DGNSS GPS CORRECTION AGE|short|range [1:300]|Maximum age of correction for GPS in DGNSS solutions|
|DGNSS GLONASS CORRECTION AGE|short|range [1:300]|Maximum age of correction for GPS in DGNSS solutions|
|DGNSS GALILEO CORRECTION AGE|short|range [1:300]|Maximum age of correction for GPS in DGNSS solutions|
|DGNSS GPS CORRECTION AGE|short|range [1:300]|Maximum age of correction for GPS in DGNSS solutions|
|DGNSS BEIDOU CORRECTION AGE|short|range [1:300]|Maximum age of correction for GPS in DGNSS solutions|
|GLONASS CORRECTIONS DATUM|byte|map<br/>0:PZ90<br/>1:PZ90.02|Glonass datum for RTCM2 corrections|
