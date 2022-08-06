import can
import os 
import asyncio
import json
from time import time
import logging

logging.basicConfig(filename='test.log', level=logging.INFO)

def can_mask_creator(can_id) -> int:
     """ Generate can mask based on lenth from can ID
     Args:
         can_id (str): can message ID (e.g CF004FE)
     Returns:
         int: return hex mask id of 0xFFFFFFF
     """
     if len(can_id) > 4:
          return int("F"*7,16)
     else:
          return int("F"*3,16)

# CAN Setting
can_interface = 'can0'

filters = [{"can_id":217056510, "can_mask": can_mask_creator('CF004FE')}]

bus = can.interface.Bus(can_interface, bustype='socketcan', can_filters=filters)

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
