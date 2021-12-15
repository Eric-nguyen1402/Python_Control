#!/usr/bin/env python3
import time
import serial
import pymysql
from datetime import datetime

time.sleep(4)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

connection = pymysql.connect(host="localhost", user="root", passwd="raspberry", database="tanker") # got to data table
cursor = connection.cursor()
x = 0.0
y = 0.0
z = 0.0
while 1:
    try:
        ans = ("get\n")
        ans = ans.encode("utf-8")
        ser.write(ans)
        readOuts = ser.readline().decode('utf-8').split(",", 4)
        # print(readOuts)
        if len(readOuts) == 4:
            x = float(readOuts[2])
            y = float(readOuts[1])
            z = float(readOuts[3])
        formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO `data_XYZ` (`X`,`Y`, `Z`,`Record_time_start`) VALUES (%s, %s, %s, %s)",(x,y,z,formatted_date))
        connection.commit()
        print("x = " + str(x),"y = " + str(y),"z = " + str(z),"time = " + str(formatted_date))
    except:
        print("error")
    time.sleep(1)
connection.close()
        

