from pyModbusTCP.client import ModbusClient
from datetime import datetime, date

import sqlite3 
import sys
import time
import struct

import numpy as np

#Take to 16bit to a 32 bit
def two16To32(first, second):
    words = [first, second]
    packed_string = struct.pack("HH", *words)
    unpacked_float = struct.unpack("f", packed_string)[0]
    return unpacked_float


SERVER_HOST = "192.168.2.250"
SERVER_PORT = 502

c = ModbusClient()


# uncomment this line to see debug message
#c.debug(True)

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)





Temp = 0
Humid = 0

    

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, read register (modbus function 0x03)
    if c.is_open():
        # read 7 registers at address 0, store result in regs list
        #regs1 = c.read_discrete_inputs(0, 8)
        #regs2 = c.read_coils(8192, 6)
        #regs3 = c.read_discrete_inputs(64, 8)
        regs4 = c.read_holding_registers(28672, 8)
        # if success display registers
        #if regs1 and regs2 and regs3 and regs4:
        if regs4:  
            #print("reg1 ad #0 to 9: "+str(regs1_temp)) 
            #print("reg2 ad #0 to 9: "+str(regs2_temp))
            #print("reg3 ad #0 to 9: "+str(regs3_temp))
            #print (two16To32(regs4_temp[0], regs4_temp[1]))
            #print (two16To32(regs4_temp[2], regs4_temp[3]))

                
            Temp = int(two16To32(regs4[0], regs4[1]))
            Humid = int(two16To32(regs4[2], regs4[3]))
            print(Temp)
            print(Humid)
              

    # sleep 30s before next polling
    time.sleep(3)

c.close()
