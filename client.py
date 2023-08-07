#!/usr/bin/env python3

""" Read 10 coils and print result on stdout. """

import time
from pyModbusTCP.client import ModbusClient

# init modbus client
c = ModbusClient(host='localhost', port=2502, auto_open=True, debug=False)

# main read loop
while True:
    # read 10 bits (= coils) at address 0, store result in coils list

    # check = c.write_multiple_registers(17, [600,50,20,1])
    # check = c.write_multiple_registers(37, [600,50,20,1])
    # check = c.write_multiple_registers(57, [600,50,20,1])
    # print("쓰기상황 : " + str(check))

    register_l = c.read_holding_registers(10, 11)
    register_ll = c.read_holding_registers(30, 11)
    register_lll = c.read_holding_registers(50, 11)

    # if success display registers
    if register_l:
        print('register: %s' % register_l)
        print('register: %s' % register_ll)
        print('register: %s' % register_lll)
    else:
        print('unable to read coils')

    # sleep 2s before next polling
    time.sleep(2)