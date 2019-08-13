__author__ = 'R.Azh'

import socket
import time

TCP_IP = 'localhost'
# TCP_IP = 'ip-ec2-instance'
TCP_PORT = 60001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

clock_start = time.clock()
time_start = time.time()

with open('received_file.text', 'wb') as f:
    print('File opend')
    while True:
        print('Receiving data...')
        data = s.recv(BUFFER_SIZE)
        print('data=%s', data)
        if not data:
            f.close()
            print('Close file')
            break
        f.write(data)

print('Successfully get the file')
f.close()
print('Connection closed')

clock_end = time.clock()
time_end = time.time()

duration_clock = clock_end - clock_start
print('clock: start = {}, end = {}, duration = {}'.format(clock_start, clock_end, duration_clock))

duration_time = time_end - time_start
print('time: start = {}, end = {}, duration = {}'.format(time_start, time_end, duration_time))
