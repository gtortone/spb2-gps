#!/usr/bin/python3

import sys
import can
import time

channel = {}
channel['gps1'] = 7
channel['gps2'] = 11
channel['clkb'] = 12
channel['hkb']  = 13

if len(sys.argv) > 3:
    busname = sys.argv[1]
    if(sys.argv[2] == 'all'):
        deviceList = ['gps1','gps2','hkb','clkb']
    else:
        deviceList = [sys.argv[2]]
    command = sys.argv[3]
else:
    print('usage: pdu <bus> <device> on/off/status')
    print(' bus: {can0, can1}')
    print(' device: { gps1, gps2, hkb, clkb }')
    sys.exit()

if (busname.lower() not in ['can0', 'can1']):
    print(f'E: bus {busname} not found')

for device in deviceList:
    if (channel.get(device) is None):
        print(f'E: device {device} not found')
        sys.exit(-1)

if (command.lower() not in ['on', 'off', 'state']):
    print(f'E: command {command} not valid for device {deviceList}')
    sys.exit(-1)

bus = can.Bus(interface="socketcan", channel=busname, bitrate=250000)

# state

if (command.lower() == 'state'):
    for device in deviceList:
        msg = can.Message(arbitration_id=0x18efcf50, data=[0x25, 0x00, channel[device], 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], is_extended_id=True)
        bus.send(msg)
        ntry = 0
        while True:
            if(ntry == 5):
                print(f"E: CAN response not received from {busname}")
                sys.exit(-1)
            rep = bus.recv(2)   # timeout 3 seconds
            if rep is not None:
                arbitrationId = hex(rep.arbitration_id)
                repid = rep.data[0]
                repch = rep.data[2]
                if(repid == 0x26 and repch == channel[device]):
                    pwstatus = (rep.data[3] & 0x0C) >> 2
                    print(f"{device} is {'ON' if pwstatus else 'OFF'}")
                    break
            ntry = ntry + 1
    sys.exit(0)        

# power on / power off

if (command.lower() == 'on'):
    power = 1
elif (command.lower() == 'off'):
    power = 0

for device in deviceList:
    msg = can.Message(arbitration_id=0x18efcf50, data=[0x01, 0x40, channel[device], power, 0xFF, 0xFF, 0xFF, 0xFF], is_extended_id=True)

    try:
        bus.send(msg)
        print(f'{device} OK')
    except can.CanError:
        print("E: {device} CAN message not sent")
