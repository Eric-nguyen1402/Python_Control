#!/usr/bin/env python3
import time
import serial
import pymysql
import os
from datetime import datetime

time.sleep(3)

ser = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 115200, timeout=1)

con_update = pymysql.connect(host="localhost", user="root", passwd="raspberry", database="tanker")
cursor_update = con_update.cursor()
 # queries for retrievint all rows

c_arr = 0  # biến counter array
arr = [0.0, 0.0]  # array
x = 0.0
y = 0.0
z = 0.0
a = 0

while 1:

    ans = ("get\n")
    ans = ans.encode("utf-8")
    ser.write(ans)
    readOuts = ser.readline().decode('utf-8').split(",", 4)
    # print(readOuts)
    if len(readOuts) == 4:
        # distance = int(readOuts[0])
        x = float(readOuts[2])
        y = float(readOuts[1])
        z = float(readOuts[3])

    update_retrive = "UPDATE `GY25` SET `X` = " + str(x) + ", `Y` = " + str(y) + ", `Z` = " + str(z) +" WHERE `GY25`.`id` = 1;"
    # executing the quires
    cursor_update.execute(update_retrive)  # chạy lệnh update
    con_update.commit()  # xác nhận update

    # print("x = " + str(x), "y = " + str(y), "z = " + str(z), "distance " + str(distance))
    
    retrive = "Select * from move_control;"
    # executing the quires
    cursor_update.execute(retrive)
    rows = cursor_update.fetchall()

    # hiệu của giá trị thứ 2 và giá trị thứ 1 nhất trong mảng
    check_connection = rows[0][1] - rows[0][0]
    level = rows[0][1]
    # print(check_connection)
    # ---------------------------------------------sét giá trị từ database chuẩn bị để gửi cho canbus-------------------------------
    if check_connection > 0:  # nếu hiệu của giá trị mảng thứ 2 và giá trị thứ 1 >= 1 thì :
             a = a + 1
             if a == 5:
                formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor_update.execute("INSERT INTO `data_XYZ` (`X`,`Y`, `Z`,`Record_time_start`,`Level`) VALUES (%s, %s, %s, %s, %s)",(x,y,z,formatted_date,level))
                con_update.commit()
                #print("x = " + str(x),"y = " + str(y),"z = " + str(z),"time = " + str(formatted_date), "level" + str(level))
                a = 0

