import serial
import threading
import time

class Controller():
    data1={}
    data2={}
    data3={}
    port ="/dev/ttyUSB0" #우분투일경우
    #port = "com1"
    baud = 19200
    serial_port = None
    alivethread = True
    t = None
    read_enable = 0

    def readthread(self):
        while(self.alivethread):
            if (self.read_enable == 1) :
                result = self.serial_port.readline()
                if len(result)>0 :
                    valueArray = str(result).split(',')
                    if len(valueArray)>=34 :

                        #데이터에 문제가 없을때만
                        count = 0
                        for k in range(1,34):
                            if valueArray[k].isdigit():
                                count=count+1
                        print(valueArray)
                        print("count:" + str(count))

                        if (count==33):

                            for i in range(1,4) :
                                for j in range(0,11) :
                                    if i==1 :
                                        self.data1.update({j+10:int(valueArray[j+1])})
                                    if i==2 :
                                        self.data2.update({j+30:int(valueArray[j+12])})
                                    if i==3 :
                                        self.data3.update({j+50:int(valueArray[j+23])})
                self.read_enable = 1

    def writeControlValue(self,data):
        self.serial_port.write(data.encode('utf-8'))
    
    def start_reading(self):
        self.t.start()
   
    def __init__(self):
        self.data1 = {10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0}
        self.data2 = {30:0,31:0,32:0,33:0,34:0,35:0,36:0,37:0,38:0,39:0,40:0}
        self.data3 = {50:0,51:0,52:0,53:0,54:0,55:0,56:0,57:0,58:0,59:0,60:0}
        self.serial_port = serial.Serial(self.port, self.baud, timeout=3)
        self.t = threading.Thread(target=self.readthread)   