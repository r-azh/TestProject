__author__ = 'R.Azh'
import socket
from threading import Thread
from socketserver import ThreadingMixIn


# other server codes can only interact with one client. If we try to connect with a second client, however,
#  it simply won't reply to the new client. To let the server interact with multiple clients,
#  we need to use multi-threading

TCP_IP = 'localhost'
# TCP_IP = socket.gethostbyaddr("your-ec2-public_ip")[0]
TCP_PORT = 60001
BUFFER_SIZE = 1024

print('TCP_IP:', TCP_IP)
print('TCP_PORT:', TCP_PORT)


class ClientThread(Thread):
    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print('New thread started for {}:{}'.format(ip, str(port)))

    def run(self):
        filename = 'mytext.text'
        f = open(filename, 'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while l:
                self.sock.send(l)
                print('sent', repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcp_sock.listen(5)
    print('Waiting for incoming connections...')
    (conn, (ip, port)) = tcp_sock.accept()
    print('Got connection from ', ip, port)
    new_thread = ClientThread(ip, port, conn)
    new_thread.start()
    threads.append(new_thread)

for t in threads:
    t.join()

