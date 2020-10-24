import socketserver
import hashlib
from socket import *
import sys

# s = socket(AF_INET,SOCK_DGRAM)
# host =sys.argv[1]
# port = 9999
# buf =1024
# addr = (host,port)
#
# file_name = sys.argv[2]
#
# bytesSend = str.encode(file_name)
# s.sendto(bytesSend,addr)
#
# f = open(file_name,"rb")
# data = f.read(buf)
# while (data):
#     if s.sendto(data,addr):
#         print("sending ...")
#         data = f.read(buf)
# s.close()
# f.close()


#nombre_archivo = ""
#hash_calculado = None

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(64*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        global minimo
        global numero_usuarios
        numero_usuarios+=1
        global nombre_archivo
        data = self.request[0].strip()
        socket = self.request[1]
        buf = 1024


        file_name = nombre_archivo

        bytesSend = str.encode(file_name)
        socket.sendto(bytesSend, self.client_address)

        f = open(file_name, "rb")
        data = f.read(buf)
        while (data):
            if socket.sendto(data, self.client_address):
                print("sending ...")
                data = f.read(buf)
        bytesSend = str.encode("fin")
        socket.sendto(bytesSend, self.client_address)
        bytesSend=str.encode(hash_calculado)
        socket.sendto(bytesSend, self.client_address)
        #socket.close()
        f.close()

if __name__ == "__main__":
    global nombre_archivo
    global hash_calculado
    global minimo
    global numero_usuarios
    numero_usuarios=0
    nombre_archivo  = input("Ingrese el nombre del archivo ")
    minimo = int(input("Ingrese el numero de usuarios en simultaneo a enviar"))
    hash_calculado = sha256sum(nombre_archivo)
    print(hash_calculado)
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()