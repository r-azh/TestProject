__author__ = 'R.Azh'
# http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
# The server is like a middle man among clients. It can queue up to 10 clients. The server broadcasts any messages
# from a client to the other participants. So, the server provides a sort of chatting room.

# In this chat code, the server is handling the sockets in non-blocking mode using select.select() method
# We pass select() three lists:
# the first contains all sockets that we might want to try reading
# the second all the sockets we might want to try writing to
# the last (normally left empty) those that we want to check for errors
# Though the select() itself is a blocking call (it's waiting for I/O completion), we can give it a timeout.
#  In the code, we set time_out = 0, and it will poll and never block.
# Actually, the select() function monitors all the client sockets and the server socket for readable activity. If any
#  of the client socket is readable then it means that one of the chat client has send a message.
# When the select function returns, the ready_to_read will be filled with an array consisting of all socket descriptors
# that are readable.
#
# In the code, we're dealing with two cases:
#
# If the master socket is readable, the server would accept the new connection.
# If any of the client socket is readable, the server would read the message, and broadcast it back to all clients
#  except the one who send the message.

import sys
import socket
import select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9009


def chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
    print('Chat server started on port ', PORT)

    while True:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for _socket in ready_to_read:
            # a new connection request recieved
            if _socket == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print('Client (%s, %s) connected' % addr)
                broadcast(server_socket, sockfd, '[%s:%s] entered our chatting room\n' % addr)

            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = _socket.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        broadcast(server_socket, _socket, '[' + str(_socket.getpeername()) + '] ' + data)
                    else:
                        # remove the socket that's broken
                        if _socket in SOCKET_LIST:
                            SOCKET_LIST.remove(_socket)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, _socket, "Client [%s, %s] is offline\n" % addr)
                except:
                    broadcast(server_socket, _socket, "Client [%s, %s] is offline\n" % addr)
                    continue


# broadcast chat messages to all connected clients
def broadcast(server_socket, _socket, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != _socket:
            try:
                socket.send(message)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

if __name__ == '__main__':
    sys.exit(chat_server())



