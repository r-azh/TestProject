import os, random
from multiprocessing import Process, Pipe

__author__ = 'R.Azh'

# A pipe consists of a mechanism that establishes communication between two endpoints
# (two processes in communication). It is a way to create a channel so as to exchange
# messages among processes.

# The official Python documentation recommends the use of a pipe for
# every two endpoints since there is no guarantee of reading safety by
# another endpoint simultaneously.


def producer_task(conn):
    value = random.randint(1, 10)
    conn.send(value)
    print('value [%d] send by pid [%d]' % (value, os.getpid()))
    conn.close()


def consumer_task(conn):
    value = conn.recv()
    print('value [%d] received by pid [%d]' % (value, os.getpid()))


####### main ############

if __name__ == '__main__':
    producer_conn, consumer_conn = Pipe()
    consumer = Process(target=consumer_task, args=(consumer_conn,))
    producer = Process(target=producer_task, args=(producer_conn,))

    consumer.start()
    producer.start()

    consumer.join()
    producer.join()