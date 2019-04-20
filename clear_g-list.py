# usage > python clear_g-list.py serialportname

# Seagate firmware commands are a combination of {Terminal Level, command id, comma separated  numeric parameters}
# total diagnostic terminal levels : [1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F, G, H, I, L and T]
# see ftp://atxlab.ddns.net/ftp/hdd/sea/man/f3-serialport-diagnostics.pdf for more nuanced insanity

import serial
import sys
import time

# delay in seconds
delay = 2

# Enter interactive mode. Starts at level T
#   this one seems to need to be all in hex to work correctly
ctrl_z = bytearray('\x1a\x0d\x0a')

# prints out state of G List, requires level T
print_glist = b'V4\r\n'

# clear the G list, also at level T
clear_glist = b'i4,1,22\r\n'

# cmd str should include the <enter> represented by \r\n
def send_cmd(serial, cmd, buff_size):
    print('writing cmd: ' + cmd)
    res_w = ser.write(cmd)
    time.sleep(delay)
    print('\twrote num bytes: ' + str(res_w))
    res_r = ser.read(buff_size)
    time.sleep(delay)
    print('\trecv num bytes: ' + str(len(res_r)))
    print('\toutput: ' + res_r)


#TODO replace with context manager
try:
    serial_port_name = sys.argv[1]
    ser = serial.Serial(serial_port_name, 38400, timeout=1)
    print('opened connection')
    time.sleep(delay)

    send_cmd(ser, ctrl_z, 32)

    send_cmd(ser, print_glist, 1084)

    send_cmd(ser, clear_glist, 1084)

    send_cmd(ser, print_glist, 1084)

    print('closing connection')
    ser.close()

except Exception as e:
    # delusions of good form
    # TODO do this properlybig_buffer = 300000
small_buffer = 1084
    print('error encountered in the serial calls')
    print(e)
finally:
    print('program exiting')
