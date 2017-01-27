#!/usr/bin/env python

import socket
import pickle
import sys
import time
import re
import json

port = 9000
host = ''
timer = 0

list = {'nodes': ('node1', 'node2', 'node3'), 
                 'lines': ('line1', 'line2')}

def recv_all(sock, size, chunk_size = 16):
    json_data = ''
    while len(json_data) < size:
        data = sock.recv(chunk_size)
        if not data:
            self.report({'ERROR'}, 
                        "Socket closed %d bytes into a %d-byte message" 
                        % (len(json_data), size))
            return None
        json_data += data
        print(json_data)
        print(len(json_data))
        return json_data

previous_time = time.time()

#list = {"node1":()}#, "node2":()}
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
    eval_str = json.loads(conn.recv(1024).decode())
    print(eval_str)
    print(eval_str == list)
    if (re.match('add', eval_str)):
        sock.send(json.dumps(eval_str))
        str = eval_str.split()
        if len(str) != 2:
            print('Error: not enougn args (add)')
            break
        for obj in objects:
            if obj.name == str[2]:
                dict = obj.as_dict
                sock.send(json.dumps(dict))
                if json.loads(recv_all(sock, size)) is None:
                    print('Error: obj was not added to server')
                    break
        print('Error: object not found')
    elif (re.match('get', eval_str) or eval_str == ''):
        if eval_str == '':
            sock.send(json.dumps('get all'))
        else:
            sock.send(json.dumps(eval_str))
        res = json.loads(recv_all(sock, size))
        if res is None:
            print('Error: smthng with get')
            break
        str = eval_str.split()
        if len(str) == 2:
            self.createObjects(res)
            break
        elif len(str) == 3:
            for obj in objects:
                if obj.name == str[1]:
                    print('%s: %s' % (str[2], obj.__dict__[str[2]]))
                    break
            break
    elif (re.match('set', eval_str)):
        if json.loads(recv_all(sock, size)) is None:
            print('Error: smthng with set')
        break
    #elif (re.match('list', eval_str)):
    elif(eval_str == 'list'):
        global list
        print('im here')
        json_data = json.dumps(list)
        size = str(len(json_data))
        print(size)
        conn.sendall(json.dumps(size).encode())
        #time.sleep(0.1)
        conn.sendall(json_data.encode())
    #conn.sendall(pickled_list)
    #if (eval_str != 'None'):
    #    print(eval_str)
    #    list = eval(eval_str)
    #else:
    #    list["node1"] = (timer, 0, 0)
    #pickled_list = pickle.dumps(list)
    #size = sys.getsizeof(pickled_list)
    #print("Size: " + str(size))

    
    #conn.send(str(size).encode())
    #time.sleep(0.1)
    #conn.sendall(pickled_list)
    #conn.send(pickled_list)
    previous_time = current_time

    #conn.close()