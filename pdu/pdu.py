#!/usr/bin/python3

import sys
import can
import time
import json

pdu = None
aliases = []
deviceList = []
command = ""

f = open("config.json", "r")
cfg = json.load(f)

for p in cfg["pdu"]:
   if p.get("alias", None) != None:
      aliases.append(p["alias"])

if len(sys.argv) > 4:

   busname = sys.argv[1]
   pdu_alias = sys.argv[2]

   if pdu_alias not in aliases: 
      print(f'E: PDU alias not found - available aliases: {aliases}') 
      sys.exit() 

   pdu = cfg["pdu"][aliases.index(pdu_alias)]

   if(sys.argv[3] == 'all'):
      deviceList = pdu["channels"].keys()
   else:
      deviceList = [sys.argv[3]]

   command = sys.argv[4]

else:
    print('usage: pdu <can_intf> <pdu_alias> <device | all> on/off/state')
    print(' bus: {can0, can1}')
    print(f' pdu_alias: {aliases}')
    sys.exit()

if (busname.lower() not in ['can0', 'can1']):
    print(f'E: bus {busname} not found')

if (command.lower() not in ['on', 'off', 'state']):
    print(f'E: command {command} not valid for device {deviceList}')
    sys.exit(-1)

bus = can.Bus(interface="socketcan", channel=busname, bitrate=250000)

can_address = 0x18ef0050 | (int(pdu["can_address"], 16) << 8)

# state

if (command.lower() == 'state'):
    for device in deviceList:
        msg = can.Message(arbitration_id=can_address, data=[0x25, 0x00, pdu["channels"][device]["id"], 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], is_extended_id=True)
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
                if(repid == 0x26 and repch == pdu["channels"][device]["id"]):
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
    msg = can.Message(arbitration_id=can_address, data=[0x01, 0x40, pdu["channels"][device]["id"], power, 0xFF, 0xFF, 0xFF, 0xFF], is_extended_id=True)

    try:
        bus.send(msg)
        print(f'{device} OK')
    except can.CanError:
        print(f"E: {device} CAN message not sent")
