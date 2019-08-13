__author__ = 'R.Azh'
import os

# Named pipes are nothing but mechanisms that allow IPC communication through
# the use of file descriptors associated with special files that implement, for instance,
# a First-In, First-Out (FIFO) scheme for writing and reading the data. Named pipes
# differ from regular pipes by the method with which they manage information.
# While the named pipes make use of the file descriptors and special files in a file
# system, regular pipes are created in memory.
# in POSIX systems, such as Linux, everything, absolutely everything, can be summed up to files. For
# each task we perform, there is  a file somewhere, and we can also find a file descriptor attached
# to it, which allows us to manipulate these files.


def write_to_named_pipe():
    named_pipe = 'my_pipe'

    if not os.path.exists(named_pipe):
        os.mkfifo(named_pipe)

    write_message(named_pipe, 'Hello World')


def write_message(input_pipe, message):
    fd = os.open(input_pipe, os.O_WRONLY)  # file descriptor
    print(message % str(os.getpid()))
    os.write(fd, (message % str(os.getpid())))
    print('...writed')
    os.close(fd)


def read_from_named_pipe():
    named_pipe = 'my_pipe'
    message = read_message(named_pipe)
    print(message)


def read_message(input_pipe):
    fd = os.open(input_pipe, os.O_RDONLY)
    print('reading...')
    message = ('I pid [%d] received a message => %s' % (os.getpid(), os.read(fd, 220)))   # 22 bytes
    os.close(fd)
    return message


write_to_named_pipe()
read_from_named_pipe()
