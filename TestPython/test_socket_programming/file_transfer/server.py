import socket
__author__ = 'R.Azh'
#  this server code can only interact with one client. If we try to connect with a second client, however,
#  it simply won't reply to the new client. To let the server interact with multiple clients,
#  we need to use multi-threading
# file transfer from a server to numerous clients.

port = 60001
s = socket.socket()
host = socket.gethostname()     # Get local machine name
print(repr(host), repr(port))
s.bind((host, port))            # Bind to the port
s.listen(5)

print('server listening ... ')

while True:
    conn, adr = s.accept()      # Establish connection with client.
    print('got connection from ', adr)
    data = conn.recv(1024)
    print('server recieved ', repr(data))

    file_name = 'mytext.text'
    f = open(file_name, 'rb')
    l = f.read(1024)
    while l:
        conn.send(l)
        print('sent ', repr(l))
        l = f.read(1024)
    f.close()

    print('Done sending')
    conn.send(b'Thank you for connecting')
    conn.close()


# For Python < 3 'strings' are in fact binary strings and 'unicode objects' are the right text objects (as they can
# contain any Unicode characters).
#
# In Python 3 unicode strings are the 'regular strings' (str) and byte strings are separate objects.
#
# Low level I/O can be done only with data (byte strings), not text (sequence of characters). For Python 2.x str was
# also the 'binary data' type. In Python 3 it is not any more and one of the special 'data' objects should be used.
#  Objects are pickled to such byte strings. If you want to enter them manually in code use the "b" prefix (b"XXX"
#  instead of "XXX").

