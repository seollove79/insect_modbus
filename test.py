import serial
import time

port = 'COM1' # 시리얼 포트
baud = 19200 # 시리얼 보드레이트(통신속도)
ser = serial.Serial(port, baud, timeout=0)

while(True) :
    result = ser.readline()
    print("결과 : " + str(result))
    time.sleep(1)