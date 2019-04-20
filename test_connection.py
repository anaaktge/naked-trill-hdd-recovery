# usage: >> python clear_g-list.py serialportname
import serial
import sys
import time

#input
# sys.argv[0] is the script name
serial_name = sys.argv[1]

# arbitrarily chosen
delay = 1.5
big_buffer = 300000
small_buffer = 1084
try:
    ser = serial.Serial(serial_name, 38400, timeout=5)

    print("checking connection is open: " + str(ser.is_open))
    time.sleep(delay)

    # should be the hex for ^Z followed by newline
    # x1A is 26 in decimal
    # x0A is 10 in decimal
    # x0D is carriage return \r
    ctrl_z = bytearray('\x1a\x0d\x0a')

    print('write ctrl z and read output')
    res_w = ser.write(ctrl_z)
    print('results of write, expected to be 3? ' + str(res_w))
    time.sleep(delay)
    res_x = ser.read(small_buffer)
    time.sleep(delay)
    print(res_x)
    print('num bytes returned: ' + str(len(res_x)))

    print('write the V4 and read output')
    print_list = bytearray('V4\r\n')
    res_w = ser.write(print_list)
    print('results of write' + str(res_w))
    time.sleep(delay) 
    res_v = ser.read(big_buffer)
    print(res_v)
    print('num bytes returned: ' + str(len(res_v)))

    print('closing connection')
    ser.close()

except Exception as e:
    print('error below encountered in the serial')
    print(e)
