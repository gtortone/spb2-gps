#!/usr/bin/python3

import sys
import can

channel = {}
channel['gps1'] = 7
channel['gps2'] = 11
channel['clkb'] = 12
channel['hkb']  = 13

if len(sys.argv) > 3:
    busname = sys.argv[1]
    device = sys.argv[2]
    command = sys.argv[3]
else:
    print('usage: pdu <bus> <device> on/off')
    print(' bus: {can0, can1}')
    print(' device: { gps1, gps2, hkb, clkb }')
    sys.exit()

if (busname.lower() not in ['can0', 'can1']):
    print(f'E: bus {busname} not found')

if (channel.get(device) is None):
    print(f'E: device {device} not found')
    sys.exit(-1)

if (command.lower() not in ['on', 'off']):
    print(f'E: command {command} not valid for device {device}')
    sys.exit(-1)

bus = can.Bus(interface="socketcan", channel=busname, bitrate=250000)    ## can0 / can1

if (command.lower() == 'on'):
    power = 1
elif (command.lower() == 'off'):
    power = 0

# cansend can0 18efcf50#01.40.0C.01.FF.FF.FF.FF
msg = can.Message(arbitration_id=0x18efcf50, data=[0x01, 0x40, channel[device], power, 0xFF, 0xFF, 0xFF, 0xFF], is_extended_id=True)

try:
    bus.send(msg)
    print('OK')
except can.CanError:
    print("E: CAN message not sent")
