import can
import os 
import asyncio
import json
from time import time
import logging

logging.basicConfig(filename='test.log', level=logging.INFO)

# CAN Setting
can_interface = 'can0'

bus = can.interface.Bus(can_interface, bustype='socketcan')

start_time = time()
list_msg_json = []

while True:
     
     msg = bus.recv()
     msg_json = json.dumps({'Timestamp':msg.timestamp, 'CAN_ID':msg.arbitration_id, "Channel":msg.channel, "Value": str([byte for byte in msg.data])})
     list_msg_json.append(msg_json)

     if (time()-start_time) >= 1:

          try:
               logging.info(list_msg_json)
               
          except Exception as e:
               logging.info(e)
          
          list_msg_json = []
          start_time = time()
