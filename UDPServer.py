import socketserver
import hashlib
import threading
import time
from datetime import datetime
import logging
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
        global logger
        numero_usuarios+=1
        global nombre_archivo
        while(numero_usuarios<minimo):
            print(numero_usuarios)
        data = self.request[0].strip()
        socket = self.request[1]
        buf = 1024
        file_name = nombre_archivo

        bytesSend = str.encode(file_name)
        socket.sendto(bytesSend, self.client_address)

        f = open(file_name, "rb")
        data = f.read(buf)
        tiempo_inicial = int(round(time.time() * 1000))
        numero_paquetes = 0
        while (data):
            if socket.sendto(data, self.client_address):
                numero_paquetes+=1
                print("sending ...")
                data = f.read(buf)
        bytesSend = str.encode("fin")
        socket.sendto(bytesSend, self.client_address)
        bytesSend=str.encode(hash_calculado)
        socket.sendto(bytesSend, self.client_address)
        #data, addr = socket.recvfrom(buf)
        tiempo_final = int(round(time.time() * 1000))
        tiempo_total = tiempo_final-tiempo_inicial
        tiempo = "tiempo: "+ str(tiempo_total)
        logger.info(tiempo)
        paquetes = "numero de fragmentos: "+ str(numero_paquetes)
        logger.info(paquetes)
        tamanio_total = numero_paquetes*buf
        tamanio = "tamaño del archivo: "+str(tamanio_total)
        logger.info(tamanio)
        #print(data.decode("utf-8"))
        #socket.close()
        f.close()

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

if __name__ == "__main__":
    global nombre_archivo
    global hash_calculado
    global minimo
    global numero_usuarios
    global hora_actual
    global file
    global logging
    now = datetime.now()
    hora_actual = now.strftime("%d-%m-%Y %H:%M:%S")
    nombre_log = hora_actual + ".txt"
    file = open(nombre_log, 'x')
    logging.basicConfig(filename=nombre_log,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logger = logging.getLogger()
    logger.info(hora_actual)
    numero_usuarios=0
    nombre_archivo  = input("Ingrese el nombre del archivo ")
    logger.info(nombre_archivo)
    minimo = int(input("Ingrese el numero de usuarios en simultaneo a enviar"))
    hash_calculado = sha256sum(nombre_archivo)
    print(hash_calculado)
    HOST, PORT = "0.0.0.0", 9999
    server = ThreadedUDPServer((HOST, PORT), MyUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, PORT))
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        file.close()
        server.shutdown()
        server.server_close()
        exit()
    # with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
    #     server.serve_forever()