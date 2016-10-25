import socket
import sys

HOST = '127.0.0.1'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'socket is created'

try:
    s.bind((HOST, PORT))
except socket.error as err:
    print 'Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1]
    sys.exit()

print 'Socket Bind HOST&PORT Success!'


s.listen(10)
print 'TCP listener ist setted up and started. Socket is now listening!'


while 1:
    conn, addr = s.accept()
    print 'Now Connected with ' + addr[0] + ':' + str(addr[1])
    buf = conn.recv(64)
    print buf
s.close()
