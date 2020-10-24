from socket import *
import sys
import select
import hashlib

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(64*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


host="localhost"
port = 9999
s = socket(AF_INET,SOCK_DGRAM)
#s.bind((host,port))

addr = (host,port)
buf=1024
s.sendto(bytes("data" + "\n", "utf-8"), (host, port))
data,addr = s.recvfrom(buf)
print ("Received File:",data.strip())
rcv_filename = data.strip().decode("utf-8")
f = open(data.strip(),'wb')

data,addr = s.recvfrom(buf)
try:
    while(data):
        f.write(data)
        s.settimeout(2)
        data,addr = s.recvfrom(buf)
        if data==str.encode("fin"):
            break
    data, addr = s.recvfrom(buf)
    print(data.decode("utf-8"))
    print(rcv_filename)
    hash_calculado=sha256sum(rcv_filename)
    print(hash_calculado)
except timeout:
    f.close()
    s.close()
    print ("File Downloaded")