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
con = sqlite3.connect('./test.db')

# uncomment this line to see debug message
#c.debug(True)

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)



with con:
    cur = con.cursor()
    #cur.execute("DROP TABLE IF EXISTS PLCValues")#change with test to see if table
    cur.execute("CREATE TABLE IF NOT EXISTS PLCValues(ID INTEGER PRIMARY KEY AUTOINCREMENT, [timestamp] timestamp, \
        x001 NUMERIC, x002 NUMERIC, x003 NUMERIC, x004 NUMERIC, x005 NUMERIC, x006 NUMERIC, x007 NUMERIC, x008 NUMERIC,\
        y001 NUMERIC, y002 NUMERIC, y003 NUMERIC, y004 NUMERIC, y005 NUMERIC, y006 NUMERIC,\
        x201 NUMERIC, x202 NUMERIC, x203 NUMERIC, x204 NUMERIC, x205 NUMERIC, x206 NUMERIC, x207 NUMERIC, x208 NUMERIC,\
        df1 REAL, df2  REAL, df3 REAL, df4 REAL)")

    Temp = 0
    Humid = 0
    count = 1
    

    while True:
        # open or reconnect TCP to server
        if not c.is_open():
            if not c.open():
                print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

        # if open() is ok, read register (modbus function 0x03)
        if c.is_open():
            # read 7 registers at address 0, store result in regs list
            regs1 = c.read_discrete_inputs(0, 8)
            regs2 = c.read_coils(8192, 6)
            regs3 = c.read_discrete_inputs(64, 8)
            regs4 = c.read_holding_registers(28672, 8)
            # if success display registers
            if regs1 and regs2 and regs3 and regs4:  
                #print("reg1 ad #0 to 9: "+str(regs1_temp)) 
                #print("reg2 ad #0 to 9: "+str(regs2_temp))
                #print("reg3 ad #0 to 9: "+str(regs3_temp))
                #print (two16To32(regs4_temp[0], regs4_temp[1]))
                #print (two16To32(regs4_temp[2], regs4_temp[3]))

                
                Temp = Temp + float(two16To32(regs4[0], regs4[1]))
                Humid = Humid + float(two16To32(regs4[2], regs4[3]))
                #print(Temp)
                #print(Humid)
                #print(count)

        # sleep 30s before next polling
        time.sleep(3)
        

        if count == 10:
            #print(Temp/10)
            #print(Humid/10)
            #null is needed for the ID INTEGER PRIMARY KEY AUTOINCREMENT to work
            cur.execute("INSERT INTO PLCValues VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",\
                (datetime.now(), \
                regs1[0], regs1[1], regs1[2], regs1[3], regs1[4], regs1[5], regs1[6], regs1[7],\
                regs2[0], regs2[1], regs2[2], regs2[3], regs2[4], regs2[5],\
                regs3[0], regs3[1], regs3[2], regs3[3], regs3[4], regs3[5], regs3[6], regs3[7],\
                Temp/10, Humid/10, 0, 0))
            print("Wrote data " + str(datetime.now()))
            
            con.commit()
            count = 0
            Temp = 0
            Humid = 0

        count += 1

con.close()
cur.close()
c.close()
