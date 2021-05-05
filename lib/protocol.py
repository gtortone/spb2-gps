#!/usr/bin/python3

import json
import yaml
import copy
import struct
import sys
import serial
from enum import Enum

class TypeError(Exception): pass
class WidthError(Exception): pass
class RangeError(Exception): pass
class MapError(Exception): pass
class FixedValueError(Exception): pass
class SerialError(Exception): pass

class DataType(Enum):
   Char = 1,
   Byte = 2,
   Short = 3,
   Integer = 4,
   Float = 5,
   Double = 6,
   Array = 7

   @classmethod
   def parse(self, str):
      if(str == 'char'):
         return DataType.Char
      if(str == 'byte'):
         return DataType.Byte
      if(str == 'short'):
         return DataType.Short
      if(str == 'integer'):
         return DataType.Integer
      if(str == 'float'):
         return DataType.Float
      if(str == 'double'):
         return DataType.Double
      if(str == 'array'):
         return DataType.Array

      return None

class Constraint(Enum):
   Fixed = 1,
   Range = 2,
   Map = 3,

   @classmethod
   def parse(self, str):
      if(str == 'fixed'):
         return Constraint.Fixed
      if(str == 'range'):
         return Constraint.Range
      if(str == 'map'):
         return Constraint.Map

      return None


ENQ = b'\x05'
ACK = b'\x06'
RESET = b'\x00'

class Item:
   def __init__(self, name):
      # SCHEMA properties
      self.name = name
      self.dataType = None
      self.position = None
      self.width = None
      self.description = None
      self.defaultValue = None
      self.constraint = None
      self.policy = None
      # range constraint
      self.minValue = None
      self.maxValue = None
      # map constraint
      self.map = []
      # CONFIGURATION properties
      self.value = None

   def checkConstraint(self, value):
      if (self.constraint == Constraint.Range):
         if (value <= self.maxValue and value >= self.minValue):
            return True
         else:
            raise RangeError("Constraint error: value range")
      elif (self.constraint == Constraint.Map):
         if (next((entry for entry in self.map if entry['value'] == value), False)):
            return True
         else:
            raise MapError("Constraint error: value not present in map")
      if (type(value) == str):
         if (len(value) <= self.width):
            return True
         else:
            raise WidthError("Constraint error: width")
      elif (self.constraint == Constraint.Fixed):
         raise FixedError("Constraint error: fixed value") 

      return False

   def assignValue(self, value):
      if (type(value) == int and (self.dataType == DataType.Short \
         or self.dataType == DataType.Byte or self.dataType == DataType.Integer)):
         if self.checkConstraint(value):
            self.value = value
            return True
      elif (type(value) == float and (self.dataType == DataType.Float \
         or self.dataType == DataType.Double)):
         if self.checkConstraint(value):
            self.value = value
            return True
      elif (type(value) == str and self.dataType == DataType.Char):
         if self.checkConstraint(value):
            self.value = value
            return True
      elif (type(value) == list and self.dataType == DataType.Array):
         if (len(value) != self.width):
            raise WidthError("Wrong array width")
            return False
         for elem in value:
            if (self.checkConstraint(elem) == False):
               return False
         self.value = value
         return True
      # user can specify a map value with a 'tag' instead of value...
      elif (type(value) == str and self.dataType == DataType.Byte):
         for entry in self.map:
            if ("tag" in entry and entry['tag'] == value):
               self.value = entry['value']
               return True
         
      return False

   def __repr__(self):
      rep = '  Item\n'
      rep += f'      name: {self.name}\n'
      rep += f'      dataType: {self.dataType}\n'
      rep += f'      position: {self.position}\n'
      rep += f'      width: {self.width}\n'
      rep += f'      description: {self.description}\n'
      if (self.defaultValue != None):
         rep += f'      defaultValue: {self.defaultValue}\n'
      if (self.policy != None):
         rep += f'      policy: {self.policy}\n'
      rep += f'      constraint: {self.constraint}\n'
      if (self.constraint == Constraint.Range):
         rep += f'         minValue: {self.minValue}\n'
         rep += f'         maxValue: {self.maxValue}\n'
      if (self.constraint == Constraint.Map):
         for entry in self.map:
            rep += f'         {entry}\n' 
      rep += f'      value: {self.value}\n'
      return rep

class Record:
   def __init__(self, cmd, name, type=None):
      self.commandCode = cmd 
      self.type = type
      self.name = name
      self.itemList = []
      self.length = 0

   def addItem(self, item):
      self.itemList.append(item)
      self.length += item.width

   def getItemByName(self, name):
      return next((item for item in self.itemList if item.name == name), False)

   """
   Check correctness of record: each mandatory item must have a value set by configuration
   (no defaultValue)

   Return value:  True - sanity check ok
                  False - sanity check failed
   """
   def checkSanity(self):
      for item in self.itemList:
         if ((item.policy == 'mandatory') and (item.value == None)):
            return False
      return True

   def __repr__(self):
      rep = f'Record(name={self.name}, type={self.type}, length={self.length})'
      return rep

class Schema:
   def __init__(self, filename):
      self.recordList = []
      self.load(filename)

   def load(self, filename):
      with open(filename) as f:
         jdoc = json.load(f)

      for record in jdoc:
         self.addRecord(record)

   def addRecord(self, record):
      if ('type' in record):
         r = Record(record['commandCode'], record['name'], record['type'])
      else:
         r = Record(record['commandCode'], record['name'])
      self.recordList.append(r)
   
      itemList = record['item']

      for item in itemList:
         i = Item(item['name'])
         i.dataType = DataType.parse(item['dataType'])
         i.position = item['position']
         i.width = item['width']
         i.description = item['description']
         if ('defaultValue' in item):
            i.defaultValue = item['defaultValue']
         if ('policy' in item):
            i.policy = item['policy']
         i.constraint = Constraint.parse(item['constraint'])   
         if (i.constraint == Constraint.Range):
            i.minValue = item['minValue'] 
            i.maxValue = item['maxValue'] 
         if (i.constraint == Constraint.Map):
            for entry in item['map']:
               i.map.append(entry)
         i.value = None
         r.addItem(i)

   def getRecordByName(self, name):
      return next((copy.deepcopy(record) for record in self.recordList if record.name == name), False)

   def getRecordByType(self, type):
      return next((copy.deepcopy(record) for record in self.recordList if record.type == type), False)   

class Config:
   def __init__(self, schema):
      self.recordList = []
      self.confData = []
      self.schema = schema

   """
   Load configuration file in YAML format
   
   Record are allocated in recordList and configuration are applied locally

   Return value:  True - if one or more item configurations are applied correctly
                  False - if none of item configurations are applied
   """
   def load(self, filename):
      with open(filename) as f:
         try:
            self.confData = yaml.load(f, Loader=yaml.FullLoader)
         except Exception as e:
            print(f"E: error reading configuration file {filename} - {e}")
            sys.exit(-1)

      for readEntry in self.confData:
         acceptRecord = False
         record = self.schema.getRecordByName(readEntry['record'])
         if (record):
            for readItem in readEntry.items():
               if (readItem[0] == 'record'): continue
               item = record.getItemByName(readItem[0])
               if (item):
                  try:
                     item.assignValue(readItem[1])
                  except Exception as e:
                     print(f"E: Config.load() record:{record.name} item:{readItem[0]} value:{readItem[1]} wrong item value - {e}")
                  else:
                     acceptRecord = True
               else:
                  print(f"E: Config.load() record:{record.name} item:{readItem[0]} wrong item name")

            if (acceptRecord):
               if record.checkSanity():
                  # copy record schema
                  self.recordList.append(record)
               else:
                  print(f"E: record:{record.name} sanity check failed")
         else:
            print(f"E: Config.load() record:{readEntry['record']} wrong record name")

      return (len(self.recordList) > 0)

class PacketBuilder:
   def encodeItem(self, value, dataType):
      retVal = bytearray()
      if (dataType == DataType.Char):
         retVal = bytes(value, 'utf-8')
      elif (dataType == DataType.Byte):
         retVal.append(value)
      elif (dataType == DataType.Short):
         retVal = struct.pack('>h', value)
      elif (dataType == DataType.Integer):
         retVal = struct.pack('>i', value)
      elif (dataType == DataType.Float):
         retVal = struct.pack('>f', value)
      elif (dataType == DataType.Double):
         retVal = struct.pack('>d', value) 
      elif (dataType == DataType.Array):
         retVal = bytearray(value)

      return retVal      

   def checksum(self, frame):
      # skip first frame element (STX)
      return (sum(frame[1:]) % 256)

   """
   Build binary frame (from a record) to send by serial

   Return value:  bytearray of encoded data 
   """
   def encodeRecord(self, record):
      frame = bytearray()
      # header of command 
      frame.append(0x02)     #  0: STX
      frame.append(0x00)     #  1: STATUS
      frame.append(record.commandCode)     #  2: PACKET TYPE
      frame.append(0x00)     #  3: LENGTH (to calculate)

      if (record.commandCode == 0x64):

         frame.append(0x00)     #  4: TRANSMISSION NUMBER
         frame.append(0x00)     #  5: PAGE INDEX
         frame.append(0x00)     #  6: MAXIMUM PAGE INDEX

         # file control information block
         frame.append(0x03)     #  7: APPLICATION FILE SPECIFICATION VERSION
         frame.append(0x00)     #  8: DEVICE TYPE (00h = all)
         frame.append(0x01)     #  9: START APPLICATION FILE FLAG (01h = apply immediately)
         frame.append(0x00)     # 10: FACTORY SETTINGS FLAG (00h = set only specified params)

         # application file record
         frame.append(record.type)
         frame.append(record.length) 

      for item in record.itemList:
         if (item.value == None):
            value = item.defaultValue
         else:
            value = item.value

         # pad string with space (fixed length string)
         if (item.dataType == DataType.Char):
            value = value.ljust(item.width)

         # encode item value
         encValue = self.encodeItem(value, item.dataType)
         frame.extend(encValue)
             
      # trailer
      length = len(frame) - 4 
      frame[3] = self.encodeItem(length, DataType.Byte)[0]

      cksum = self.encodeItem(self.checksum(frame), DataType.Byte)
      frame.extend(cksum)    #  CHECKSUM
      frame.append(0x03)     #  ETX

      return frame

   def print(self, frame):
      s = frame.hex()
      print(' '.join(s[i:i+2] for i in range(0, len(s), 2)))
   
class SerialChannel:
   def __init__(self, port, baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE):
      try:
         self.serial = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout=1)
      except Exception as e:
         print(f"E: error opening serial port {port} - {e}")
         sys.exit(-1)

      if (self.reset() == False):
         print(f"E: error resetting serial port {port}")
         sys.exit(-1)
   
   def enquiry(self):
      self.serial.write(ENQ)
      res = self.serial.read(1)
      if (res == ACK):
         return True

      return False

   def reset(self):
      for i in range(1,256):
         self.serial.write(RESET)
         if (self.enquiry()):
            return True

      return False 
      
   def sendFrame(self, frame):
      if (self.reset()):
         self.serial.write(frame)
         res = self.serial.read(1)
         if (res == b''):
            raise SerialError(f"sendFrame error: frame not acknowledge")
         elif (res != ACK):
            raise SerialError(f"sendFrame error: frame not acknowledge - {ord(res)}")
      else:
         raise SerialError(f"sendFrame error: device busy or not connected")
