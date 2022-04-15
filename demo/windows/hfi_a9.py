#!/usr/bin/env python
# -*- coding:utf-8 -*-
import binascii
import math
import serial
import struct
import time
import sys
#import imp
if sys.getdefaultencoding() != 'utf-8':
    imp.reload(sys)
    sys.setdefaultencoding('utf-8')

def receive_split(receive_buffer):
    buff = []
    for i in range(0, len(receive_buffer), 2):
        buff.append(receive_buffer[i:i + 2])
    return buff


def hex_to_ieee(len, buff):
    str = b''
    data = []
    for i in range(len // 2 - 3, 11, -4):
        for j in range(i, i - 4, -1):
            str += buff[j]            
        #data.append(struct.unpack('>f', str.decode('hex'))[0])
        data.append(struct.unpack('>f', bytes.fromhex(str.decode('UTF-8')))[0])
        #print(str)
        str = b''
    data.reverse()
    return data


if __name__ == "__main__":

    try:
        hf_imu = serial.Serial(port='COM21', baudrate=921600, timeout=0.5)
        if hf_imu.isOpen():
            print ("imu connect success")
        else:
            hf_imu.open()
            print ("imu is open")

    except Exception as e:
        print (e)
        print ("Can't find ComPort, please check if imu is connected to the computer")
        exit()

    else:
        
        sensor_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while True:
            count = hf_imu.inWaiting()
            if count > 24:
                # bytearray() The method returns a new byte array.
                # The elements in this array are mutable, and each element has a range of values: 0 <= x < 256
                receive_buffer = bytearray()
                receive_buffer = binascii.b2a_hex(hf_imu.read(count))
                receive_len = len(receive_buffer)
                buff = receive_split(receive_buffer)                                

                if buff[0]+buff[1]+buff[2] == b'aa552c':
                    sensor_data = hex_to_ieee(receive_len, buff)

                if buff[0]+buff[1]+buff[2] == b'aa5514':
                    rpy = hex_to_ieee(receive_len, buff)

                    print ('Acceleration :')
                    print('\t x_acc：' + "%.2f g" % sensor_data[3])
                    print('\t y_acc：' + "%.2f g" % sensor_data[4])
                    print('\t z_acc：' + "%.2f g" % sensor_data[5] + "\r\n")

                    print ('Angular velocity：')
                    print ('\t x_vel：' + "%.2f rad/s" % (sensor_data[0] * -9.8))
                    print ('\t y_vel：' + "%.2f rad/s" % (sensor_data[1] * -9.8))
                    print ('\t z_vel：' + "%.2f rad/s" % (sensor_data[2] * -9.8) + "\r\n")

                    print ('Angle：')
                    print ('\t x_angle：' + "%.2f °" % rpy[0])
                    print ('\t y_angle：' + "%.2f °" % (- rpy[1]))
                    print ('\t z_angle：' + "%.2f °" % (- rpy[2] + 180) + "\r\n")

                    print ('Magnetic Field：')
                    print ('\t x_mag：' + "%.0f mG" % (sensor_data[6] * 1000))
                    print ('\t y_mag：' + "%.0f mG" % (sensor_data[7] * 1000))
                    print ('\t z_mag：' + "%.0f mG" % (sensor_data[8] * 1000) + "\r\n")


            time.sleep(0.001)

