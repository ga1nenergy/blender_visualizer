#!/usr/bin/env python

import socket
import pickle
import sys
import time

port = 9000
host = ''
timer = 0

previous_time = time.time()

list = {"node1":()}#, "node2":()}
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', port))

while True:
    sock.listen(1)
    print("Listening port: " + str(port))
    conn, addr = sock.accept()
    print('Connected:' + str(addr))
    current_time = time.time()
    print("current_time: {0}".format(current_time))
    timer += current_time - previous_time
    eval_str = (conn.recv(1024)).decode()
    print(eval_str)
    if (eval_str != 'None'):
        print(eval_str)
        list = eval(eval_str)
    else:
        list["node1"] = (timer, 0, 0)
        #list["node2"] = (0, timer, 0)
    pickled_list = pickle.dumps(list)
    size = sys.getsizeof(pickled_list)
    print("Size: " + str(size))

    
    conn.send(str(size).encode())
    time.sleep(0.1)
    conn.sendall(pickled_list)
    #conn.send(pickled_list)
    previous_time = current_time

    conn.close()