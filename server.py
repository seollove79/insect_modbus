import argparse
from pyModbusTCP.server import ModbusServer, DataBank
from datetime import datetime
import Controller
import threading
import time

class MyDataBank(DataBank):
    """A custom ModbusServerDataBank for override get_holding_registers method."""

    def __init__(self):
        # turn off allocation of memory for standard modbus object types
        # only "holding registers" space will be replaced by dynamic build values.
        super().__init__(virtual_mode=True)
        self.sensor_data = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,
                            10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,
                            20:0,21:0,22:0,23:0,24:0,25:0,26:0,27:0,28:0,29:0,
                            30:0,31:0,32:0,33:0,34:0,35:0,36:0,37:0,38:0,39:0,
                            40:0,41:0,42:0,43:0,44:0,45:0,46:0,47:0,48:0,49:0,
                            50:0,51:0,52:0,53:0,54:0,55:0,56:0,57:0,58:0,59:0,
                            60:0,61:0,62:0,63:0,64:0,65:0,66:0,67:0,68:0,69:0,
                            70:0,71:0,72:0,73:0,74:0,75:0,76:0,77:0,78:0,79:0,
                            80:0,81:0,82:0,83:0,84:0,85:0,86:0,87:0,88:0,89:0,
                            90:0,91:0,92:0,93:0,94:0,95:0,96:0,97:0,98:0,99:0}


    def get_holding_registers(self, address, number=1, srv_info=None):
        """Get virtual holding registers."""
        # populate virtual registers dict with current datetime values
        now = datetime.now()
        # build a list of virtual regs to return to server data handler
        # return None if any of virtual registers is missing
        v_regs_d = self.sensor_data

        try:
            return [v_regs_d[a] for a in range(address, address+number)]
        except KeyError:
            return
        
    def set_holding_registers(self, address, word_list, srv_info=None):
        for idx,item in enumerate(word_list):
            target_address = address + idx
            self.sensor_data.update({target_address:item})
        return True
    
if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default='0.0.0.0', help='Host (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=2502, help='TCP port (default: 2502)')
    args = parser.parse_args()
    # init modbus server and start it
    myDataBank = MyDataBank()
    server = ModbusServer(host=args.host, port=args.port, data_bank=myDataBank)
    controller = Controller.Controller()
    controller.start_reading()
    
    def writethread():
        while True :
            #장치의 제어값 만들기
            controlValue01 = '@,1,' + changeNumber(myDataBank.sensor_data[7]) + ',' + changeNumber(myDataBank.sensor_data[8])  + ',' + changeNumber(myDataBank.sensor_data[9]) + ',' + changeNumber(myDataBank.sensor_data[10]) + '\r\n'
            controlValue02 = '@,2,' + changeNumber(myDataBank.sensor_data[27]) + ',' + changeNumber(myDataBank.sensor_data[28])  + ',' + changeNumber(myDataBank.sensor_data[29]) + ',' + changeNumber(myDataBank.sensor_data[30]) + '\r\n'
            controlValue03 = '@,3,' + changeNumber(myDataBank.sensor_data[47]) + ',' + changeNumber(myDataBank.sensor_data[48])  + ',' + changeNumber(myDataBank.sensor_data[49]) + ',' + changeNumber(myDataBank.sensor_data[50]) + '\r\n'
        
            #장치의 제어값 보드에 쓰기
            controller.writeControlValue(controlValue01)
            controller.writeControlValue(controlValue02)
            controller.writeControlValue(controlValue03)

            time.sleep(3)

            myDataBank.sensor_data.update(controller.data1)
            myDataBank.sensor_data.update(controller.data2)
            myDataBank.sensor_data.update(controller.data3)

    def changeNumber(numberValue):
        returnNumberStr = ""
        length = len(str(numberValue))
        for i in range (4-length) :
            returnNumberStr += '0'
        returnNumberStr += str(numberValue)
        return returnNumberStr

    t = threading.Thread(target=writethread)
    t.start()

    server.start()