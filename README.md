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
|SV SELECTION|array[10]|map<br/>0:Heed health<br/>1:Disable satellite<br/>2:Enable satellite regardless good or bad health|[0,1,2,6]: 0<br/>[3,4,5,7,8,9]: 1|Enable/disable SV|

### GALILEO SV selection 

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|SV SELECTION|array[36]|map<br/>0:Heed health<br/>1:Disable satellite<br/>2:Enable satellite regardless good or bad health|[0..35]: 0|Enable/disable SV|

### BEIDOU SV selection 

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|SV SELECTION|array[63]|map<br/>0:Heed health<br/>1:Disable satellite<br/>2:Enable satellite regardless good or bad health|[0..62]: 0|Enable/disable SV|

### Output Message

|item name|type|constraint|default value|description|
|-|-|-|-|-|
|OUTPUT MESSAGE TYPE|byte|map<br/>6:NMEA_GGA<br/>7:NMEA_GGK<br/>8:NMEA_ZDA<br/>11:1PPS<br/>12:NMEA_VTG<br/>13:NMEA_GST<br/>14:NMEA_PJK<br/>15:NMEA_PJT<br/>16:NMEA_VGK<br/>17:NMEA_VHD<br/>18:NMEA_GSV<br/>19:NMEA_TSN<br/>20:NMEA_TSS<br/>21:NMEA_PRC<br/>22:NMEA_REF<br/>23:NMEA_GGK_SYNC<br/>29:NMEA_AVR<br/>31:NMEA_HDT<br/>32:NMEA_ROT<br/>33:NMEA_ADV<br/>34:NMEA_PIO<br/>35:NMEA_BETA<br/>37:NMEA_VRSGGA<br/>38:NMEA_GSA<br/>40:NMEA_RMC<br/>41:NMEA_BPQ<br/>44:NMEA_GLL<br/>45:NMEA_GRS<br/>47:NMEA_LDG|-|Type of message or packet|
|PORT INDEX|byte|map<br/>0:Serial port COM1<br/>1:Serial port COM2|-|Port number|
|FREQUENCY|byte|map<br/>0:Off<br/>1:10 Hz<br/>2:5 Hz<br/>3:1 Hz<br/>4:2 seconds<br/>5:5 seconds<br/>6:10 seconds<br/>7:30 seconds<br/>8:1 minute<br/>9:5 minutes<br/>10:10 minutes<br/>11:2 Hz<br/>12:15 seconds<br/>13:20 Hz<br/>15:50 Hz<br/>|-|Frequency|
|OFFSET|byte|range [0:255]|0|Offset in seconds from scheduled output rate|





