#!/usr/bin/python3

import sys
import time
import gpiod

pin = {}
pin['gps1'] = 3    # GPS1 Linux pin 1023
pin['gps2'] = 2    # GPS2 Linux pin 1022

cmd = {}
cmd['gps1'] = ['enable', 'disable']
cmd['gps2'] = ['enable', 'disable']

if len(sys.argv) > 2:
    device = sys.argv[1]
    command = sys.argv[2]
else:
    print('usage: gpscomm <device> <command>')
    print('device: gps1 - commands: enable/disable')
    print('device: gps2 - commands: enable/disable')
    sys.exit()

if (cmd.get(device) is None):
    print(f'E: device {device} not found')
    sys.exit(-1)

cmdList = cmd.get(device)
if (command not in cmdList):
    print(f'E: command {command} not found for device {device}')
    sys.exit(-1)

chip = gpiod.chip('gpiochip0', gpiod.chip.OPEN_BY_NAME)

#pinName = pin.get(device);
line = chip.get_line(pin[device])

if (line is None):
    print(f'E: gpio pin {pinName} not found')
    sys.exit(-1)

config = gpiod.line_request()
config.consumer = "foobar"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT

line.request(config)

if (command == 'enable'):
    line.set_value(1)
elif (command == 'disable'):
    line.set_value(0)

print('OK')
