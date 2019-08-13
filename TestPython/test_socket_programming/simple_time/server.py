__author__ = 'R.Azh'
import socket
import time

# the server sends the current time string to the client

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
server_socket.bind((host, port))

# queue up to 5 requests
server_socket.listen(5)

while True:
    # establish a connection
    client_socket, adr = server_socket.accept()

    print("Got a connection from %s" % str(adr))
    current_time = time.ctime(time.time()) + "\r\n"
    client_socket.send(current_time.encode('ascii'))
    client_socket.close()
