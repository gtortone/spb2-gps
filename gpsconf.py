#!/usr/bin/python3

import os
import argparse
from lib.protocol import *

basedir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="=== Trimble BX992 configuration tool ===")
parser.add_argument('--port', action='store', type=str, help='serial port device (default: /dev/ttyUL1)', default='/dev/ttyUL1')
parser.add_argument('--speed', action='store', type=int, help='serial port speed (default: 115200)', default=115200)
parser.add_argument('--bit', action='store', type=int, help='serial port bits (default: 8)', choices=[7, 8], default=8)
parser.add_argument('--parity', action='store', type=str, help='serial port parity (default: N)', choices=['O', 'E', 'N'], default='N')
parser.add_argument('--stop', action='store', type=int, help='serial port stop bits (default: 1)', choices=[1, 2], default='1')
parser.add_argument('--file', action='store', type=str, help='configuration file (required)', required=True)
parser.add_argument('--verbose', action='store_true', help='verbose execution with frame dump')
args = parser.parse_args()

# serial
ser = SerialChannel(port=args.port, baudrate=args.speed, bytesize=args.bit, parity=args.parity, stopbits=args.stop)

# protocol schema
schema = Schema(basedir + '/schema/Trimble-BX992.json')
config = Config(schema)

# configuration file
rval = config.load(args.file)

if(rval):
   print("Configuration built successfully !")

pb = PacketBuilder()

nerr = 0
for record in config.recordList:
   frame = pb.encodeRecord(record)
   print(record.name)
   if(args.verbose):
      pb.print(frame)
      print('---')
   try:   
      ser.sendFrame(frame)
   except Exception as e:
      print(f"E: error sending frame: {e}")
      nerr = nerr + 1

print(f"Configuration finished with {nerr} errors on {len(config.recordList)} frames")

