# có kiểm tra biến bắt đầu/dừng lưu các giá trị vị trí 
import serial
import time
import string
import pymysql  # database
import datetime

time.sleep(3)
con_update = pymysql.connect(host="localhost", user="root", passwd="raspberry", database="tanker")
cursor_update = con_update.cursor()

lat = 0.000000
lng = 0.000000
i  = 0

def convert_lat_to_degrees(raw_value, sign):
    dd = int(raw_value/100)
    ss = raw_value - (dd * 100)
    LatDec = dd + ss / 60
    if sign == "S":
        LatDec = LatDec *(-1)
    position = "%.6f" % (LatDec)
    return position

def convert_lng_to_degrees(raw_value, sign):
    dd = int(raw_value/100)
    ss = raw_value - (dd * 100)
    LngDec = dd + ss / 60
    if sign == "W":
        LngDec = LngDec *(-1)
    position = "%.6f" % (LngDec)
    return position

while 1:
    con_read = pymysql.connect(host="localhost", user="root", passwd="raspberry", database="tanker")
    cursor_read = con_read.cursor()
    cmt_read = "SELECT * FROM `GY25` WHERE 1;"
    
    cursor_read.execute(cmt_read)
    rows = cursor_read.fetchall()
    
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    newdata = ser.readline()
    print(newdata)
    if str(newdata[0:6]) == "b'$GPRMC'":
        newdata = str(newdata.decode()).replace("\r\n", "").split(",", 12)
        # print(newdata)
        if newdata[3] != "":

            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # take time to add to database
            
            lat = float(newdata[3])
            lat_minus_plus = newdata[4]
            lng = float(newdata[5])
            lng_minus_plus = newdata[6]

            lat_in_degrees = convert_lat_to_degrees(lat, lat_minus_plus)
            lon_in_degrees = convert_lng_to_degrees(lng, lng_minus_plus)
            
            print("Lat:" + str(lat_in_degrees) + " lng:" + str(lon_in_degrees))
            
            update_retrive = "UPDATE `GY25` SET `latitude` = " + str(lat_in_degrees) + ", `longitude` = " + str(lon_in_degrees) + " WHERE `GY25`.`id` = 1;"
            
            # executing the quires
            cursor_update.execute(update_retrive)  # chạy lệnh update
            con_update.commit()  # xác nhận update
            
            retrive = "Select * from move_control;"
            cursor_update.execute(retrive)
            rows = cursor_update.fetchall()
            check_connection = rows[0][1] - rows[0][0]
            level = rows[0][1]
            i += 1
            if i >= 10 and rows[0][6] == 1:
                #executing the quires
                cursor_update.execute("INSERT INTO record_data (lat, lng) VALUES (%s, %s)",(lat_in_degrees, lon_in_degrees))  # chạy lệnh update
                con_update.commit()  # xác nhận update
                i=0
                # print("save")
            if check_connection != -1:
                  cursor_update.execute("INSERT INTO `data_map` (`lat`,`lng`, `level`) VALUES (%s, %s, %s)",(lat_in_degrees, lon_in_degrees, level))
                  con_update.commit()  # xác nhận update


