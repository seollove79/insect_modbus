import serial
import threading
import time

class Controller():

    data1={}
    data2={}
    data3={}
    port ="com1"
    baud = 19200
    serial_port = None
    alivethread = True
   
    def __init__(self):
        self.data1 = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0}
        self.data2 = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0}
        self.data3 = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0}
        self.serial_port = serial.Serial(self.port, self.baud, timeout=3)

    def readthread(self):


