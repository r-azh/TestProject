import socket

__author__ = 'R.Azh'

port = 60001
s = socket.socket()
host = socket.gethostname()  # Get local machine name
print(repr(host), repr(port))
s.connect((host, port))         # connect not bind !!! bind is for server connect is for client

s.send(b"Hello server!")

with open('received_file.text', mode='wb') as f:
    print('File opened')
    while True:
        print('Receiving data...')
        data = s.recv(1024)
        print('data=%s', data)
        if not data:
            break
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('Connection closed')
