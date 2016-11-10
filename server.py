#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys

HOST = '134.155.194.136'
PORT = 2222

# Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind HOST&PORT Socket
try:
    s.bind((HOST, PORT))
except socket.error as err:
    print 'Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1]
    sys.exit()
# Setup and Start TCP listener
# Socket start listening
s.listen(10)

while 1:
    conn, addr = s.accept()
    print conn
    print addr
    print 'Now Connected with ' + addr[0] + ':' + str(addr[1])
    # Receive data from socket
    data_recv = conn.recv(1024)
    if not data_recv: break
    # Send data to socket client
    data_send = "thank you"
    conn.sendall(data_send)

    print "i got", data_recv
    print "i sent", data_send

    recvlist = data_recv.split(',')
    i = 1
    for l in recvlist:
        print i, l
        i = i +1

    conn.close()
s.close()
