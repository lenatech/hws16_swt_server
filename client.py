import socket
import sys
import json

HOST = 'Replace your IP here'
PORT = 2222

s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)
## SOME expected JSON format query from USER
json6 = "QLM8FNZJ"
json7 = "{\"Avocado\": 1,\"Bananas\":1,\"Egg\":1}"
json8 = "{\"Avocado\": 1,\"Bananas\":1,\"Egg\":0}"
s.sendall(json6)
s.sendall(json7)
s.sendall(json8)

data = s.recv(99999999)
s.close()
print data
