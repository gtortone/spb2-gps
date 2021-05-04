# Trimble BX992
Python library for Trimble BX992 GPS receiver configuration

## Introduction
Trimble GPS receiver can be configured through a serial link with binary format commands (https://www.trimble.com/OEM_ReceiverHelp)
The `gpsconf.py` Python script accepts a YAML (https://en.wikipedia.org/wiki/YAML) configuration file where each record is a set of
parameters (items) to configure. Configuration items will be encoded and sent by serial link to the receiver.

## Record and item names

### General Controls

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|ELEVATION MASK|byte|range [0:90]|0|Elevation mask in degrees|
|PDOP MASK|byte|range [0:255]|99|Position Dilution of Precision Mask|
|RTK POSITIONING MODE|byte|map<br/>0:synchronous<br/>1:low latency|1|RTK positioning mode|
|POSITIONING SOLUTION SELECTION|byte|map<br/>0:Use best available solution<br/>1:Produce DGPS and autonomous solutions<br/>2:Produce DGPS, RTK float and autonomous solutions<br/>3:Produce RTK fix, DGPS and Autonomous solutions|0|Controls use of DGPS and RTK solutions|
|DGNSS GPS CORRECTION AGE|short|range [1:300]|60|Maximum age of correction for GPS in DGNSS solutions|
|DGNSS GLONASS CORRECTION AGE|short|range [1:300]|60|Maximum age of correction for GPS in DGNSS solutions|
|DGNSS GALILEO CORRECTION AGE|short|range [1:300]|60|Maximum age of correction for GPS in DGNSS solutions|
|DGNSS GPS CORRECTION AGE|short|range [1:300]|60|Maximum age of correction for GPS in DGNSS solutions|
|DGNSS BEIDOU CORRECTION AGE|short|range [1:300]|60|Maximum age of correction for GPS in DGNSS solutions|
|GLONASS CORRECTIONS DATUM|byte|map<br/>0:PZ90<br/>1:PZ90.02|0|Glonass datum for RTCM2 corrections|
|AUTONOMOUS DIFFERENTIAL ENGINE MODE|byte|map<br/>0:least squares<br/>1:Kalman filter<br/>2:Kalman filter with SBAS+|0|Filter selection|
|RECEIVER MOTION|byte|map<br/>0:Kinematic<br/>1:Human portable<br/>2:Mapping vehicle<br/>3:Off-road vehicle<br/>4:Heavy equipment<br/>5:Farm equipment<br/>6:Airborne rotor<br/>7:Airborne fixed wing<br/>8:Marine<br/>9:Rail<br/>11:Automotive<br/>33:Static|11|Receiver motion|
|RTK PROPAGATION LIMIT|byte|map<br/>10:10 seconds<br/>20:20 seconds<br/>40:40 seconds<br/>60:60 seconds<br/>120:120 seconds<br/>|20|RTK propagation limit|

### Serial Port

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|SERIAL PORT INDEX|byte|map<br/>0:Serial port COM1<br/>1:Serial port COM2|-|The number of serial port to configure|
|BAUD RATE|byte|map<br/>0:9600 baud<br/>1:2400 baud<br/>2:4800 baud<br/>4:19200 baud<br/>5:38400 baud<br/>6:57600 baud<br/>7:115200 baud<br/>8:300 baud<br/>9:600 baud<br/>10:1200<br/>11:230000 baud<br/>12:460000 baud|7|Data transmission rate|
|PARITY|byte|map<br/>0:No parity<br/>1:Odd parity<br/>2:Even parity|0|Parity in transmission|
|FLOW CONTROL|byte|map<br/>0:No flow control<br/>1:CTS flow control|0|Flow control|

### GPS SV selection 

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|SV SELECTION|array[32]|map<br/>0:Heed health<br/>1:Disable satellite<br/>2:Enable satellite regardless good or bad health|[0..31]: 0|Enable/disable SV|

### GLONASS SV selection 

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|SV SELECTION|array[24]|map<br/>0:Heed health<br/>1:Disable satellite<br/>2:Enable satellite regardless good or bad health|[0..23]: 0|Enable/disable SV|

### IRNSS SV selection 

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|SV SELECTION|array[14]|map<br/>0:Heed health<br/>1:Disable satellite<br/>2:Enable satellite regardless good or bad health|[0..13]: 0|Enable/disable SV|

### QZSS SV selection 

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|SV SELECTION|array[10]|map<br/>0:Heed health<br/>1:Disable satellite<br/>2:Enable satellite regardless good or bad health|[0..9]: 0|Enable/disable SV|

### GALILEO SV selection 

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|SV SELECTION|array[36]|map<br/>0:Heed health<br/>1:Disable satellite<br/>2:Enable satellite regardless good or bad health|[0..35]: 0|Enable/disable SV|

### BEIDOU SV selection 

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|SV SELECTION|array[63]|map<br/>0:Heed health<br/>1:Disable satellite<br/>2:Enable satellite regardless good or bad health|[0..62]: 0|Enable/disable SV|




