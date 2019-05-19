#usage: > python translator_corruptor.py serialportname startingLBAaddress totalentriestoadd

# Seagate firmware commands are a combination of {Terminal Level, command id, comma separated  numeric parameters}
# total diagnostic terminal levels : [1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F, G, H, I, L and T]
# see ftp://atxlab.ddns.net/ftp/hdd/sea/man/f3-serialport-diagnostics.pdf for more nuanced insanity

import random
import serial
import sys
import time

#CLI input processing 
# sys.argv[0] is the script name
serial_port_name = sys.argv[1]
starting_addr = int(sys.argv[2])
total_entries_to_add = int(sys.argv[3])

# unabashedly arbitrary
small_buffer = 32
large_buffer = 5000
delay = 1.5 # 1.0 seems to be slightly too fast

# Firware command strings
# Enter diagnostic interactive mode. Starts at level T
#   this one seems to need to be all in hex to work correctly
ctrl_z = bytearray('\x1a\x0d\x0a')
# prints out state of G List, requires level T

print_glist = b'V4\r\n'

# change terminal level to level 2
go_to_T2 = b'/2\r\n'

# change terminal level to T
go_to_T = b'/T\r\n'

# Modify Track Defect List, requires level T2
add_defect_cmd = b'F'
add_defect_params = b',a1\r\n'

# cmd str should include the <enter> represented by \r\n to execute on the drive
def send_cmd(serial, buff_size, cmd, console_msg=""):
    print('writing cmd to firmware: ' + cmd)
    print("\t"+console_msg)
    res_w = ser.write(cmd)
    time.sleep(delay)
    print('\tsent bytes: ' + str(res_w))
    res_r = ser.read(buff_size)
    time.sleep(delay)
    print('\trecv bytes: ' + str(len(res_r)))
    print('\trecv msg: ' + res_r)


#TODO replace with a context manager to properly handle failures and close properly
#TODO make into proper module and wrap into a function ?
try:
    #TODO make serial name into a cmd line argument
    print("opening serial connection to " + serial_port_name)
    ser = serial.Serial(serial_port_name, 38400, timeout=1)
    # seems to need a longer one at start
    time.sleep(delay*2)

    send_cmd(ser, small_buffer, ctrl_z, "ctrl-Z")
    #send_cmd(ser, print_glist, large_buffer)
    send_cmd(ser, small_buffer, go_to_T2, "change terminal level")

    # Send the Add defects cmd for each desired entry
    
    curr_addr = starting_addr

    for i in range(0, total_entries_to_add):
        increment = random.randint(2,12)
        curr_addr = curr_addr + increment
        full_add_defect = bytearray(add_defect_cmd + str(curr_addr) + add_defect_params)
        print("record #" + str(i) + "/" + str(total_entries_to_add))
        send_cmd(ser, small_buffer, full_add_defect, "adding to glist")
    
    # check that they really were added
    # TODO if a lot were added this can take many minutes to execute
    send_cmd(ser, small_buffer,  go_to_T, "change terminal level")
    send_cmd(ser, large_buffer, print_glist, "print updatd list")

    print('closing connection')
    ser.close()
except Exception as e:
    # pretensions to good form
    print('error below encountered in the serial')
    print(e)
finally:
    print('exiting')
