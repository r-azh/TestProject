__author__ = 'R.Azh'

# The basic mechanisms of client-server setup are:

# A client app send a request to a server app.
# The server app returns a reply.
# Some of the basic data communications between client and server are:
#   - File transfer - sends name and gets a file.
#   - Web page - sends url and gets a page.
#   - Echo - sends a message and gets it back.

# Server Socket
# - create a socket - Get the file descriptor!
# - bind to an address -What port am I on?
# - listen on a port, and wait for a connection to be established.
# - accept the connection from a client.
# - send/recv - the same way we read and write for a file.
# - shutdown to end read/write.
# - close to releases data.


# Client Socket
# - create a socket.
# - bind* - this is probably be unnecessary because you're the client, not the server.
# - connect to a server.
# - send/recv - repeat until we have or receive data
# - shutdown to end read/write.
# - close to releases data.
