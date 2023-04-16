import serial
import threading
import time

class Controller():
    data1={}
    data2={}
    data3={}
    port ="ttyUSB0"
    baud = 19200
    serial_port = None
    alivethread = True
    t = None

    def readthread(self):
        while(self.alivethread):
            result = self.serial_port.readline()
            if len(result)>0 :
                valueArray = str(result).split(',')
                if len(valueArray)>=34 :

                    #데이터에 문제가 없을때만
                    count = 0
                    for k in range(1,34):
                        if valueArray[k].isdigit():
                            count=count+1

                    if (count==33):
                        for i in range(1,4) :
                            for j in range(0,11) :
                                if i==1 :
                                    self.data1.update({j:int(valueArray[j+1])})
                                if i==2 :
                                    self.data2.update({j+20:int(valueArray[j+12])})
                                if i==3 :
                                    self.data3.update({j+40:int(valueArray[j+23])})
            time.sleep(3)

    def writeControlValue(self,data):
        self.serial_port.write(data.encode('utf-8'))
    
    def start_reading(self):
        self.t.start()
   
    def __init__(self):
        self.data1 = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
        self.data2 = {20:0,21:0,22:0,23:0,24:0,25:0,26:0,27:0,28:0,29:0,30:0}
        self.data3 = {40:0,41:0,42:0,43:0,44:0,45:0,46:0,47:0,48:0,49:0,50:0}
        self.serial_port = serial.Serial(self.port, self.baud, timeout=3)
        self.t = threading.Thread(target=self.readthread)   