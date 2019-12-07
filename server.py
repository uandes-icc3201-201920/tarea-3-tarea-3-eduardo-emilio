#server
import socket
import sys
import _thread
import random

# ('tipo comando *parametro* *parametro*')
# tipo 0-2    0 quit... 2 insert 02221 grosere

basededatos = {102: "dr. stone", 122: "no tan rapido kaiba",
                1200: 'kirito',
                123: "yonebayashi no maid dragon",
                321: "emo boy que no quiere madurar #un shonen cualquiera",
                358: "me aburri"
                }

criesInDepression = random.randint(1000, 10000)  # contador global
while (criesInDepression in basededatos):
    criesInDepression = random.random(1000, 10000)

lock= _thread.allocate_lock()

def asistir_cliente(coneccion, dir_cliente):
    while True:
        global criesInDepression
        request = coneccion.recv(4096).decode().split("/@")
        tipo = int(request[0])
        if tipo == 0:
            if request[1] == 'disconnect':
                break
            elif request[1] == 'quit':
                break
            elif request[1] == 'list':
                response = list(basededatos.keys())
                respon='['
                for i in response:
                    respon += str(i)+','
                respon +=']'
                coneccion.sendall(respon.encode())

        elif tipo == 1:
            if request[1] == 'insert':
            lock.acquire()
            # seccion critica escritura
                basededatos[criesInDepression] = request[2]
                coneccion.sendall(str(criesInDepression).encode())
                criesInDepression += 1
            # fin seccion critica
            lock.release()

            elif request[1] == 'get':
                key = int(request[2])
                if key not in basededatos:
                    coneccion.sendall("ERRROR: la llave no existe".encode())
                else:
                    coneccion.sendall(str(basededatos[key]).encode())
            elif request[1] == 'peek':
                if int(request[2]) in basededatos:
                    coneccion.sendall("True".encode())
                else:
                    coneccion.sendall("False".encode())
            elif request[1] == 'delete':
                lock.acquire()
                if int(request[2]) in basededatos:
                    basededatos.pop(int(request[2]))
                    coneccion.sendall("eliminado con exito".encode())
                else:
                    coneccion.sendall("ERROR: la llave no existe".encode())
                lock.release()
        else:
            if request[1]=='update':
                lock.acquire()
                if int(request[2]) in basededatos:
                    basededatos[int(request[2])] = request[3]
                    coneccion.sendall("actualizacion exitosa".encode())
                else:
                    coneccion.sendall("ERROR: la llave no existe".encode())
                lock.release()
            else: 
                lock.acquire()
                if int(request[2]) in basededatos:
                    coneccion.sendall("ERROR: la llave ya existe".encode())
                else:
                    basededatos[int(request[2])] = request[3]
                    coneccion.sendall("insercion exitosa".encode())
                lock.release()
    coneccion.close()

argv = list(sys.argv)
rutasocket = "/tmp/db.tuples.sock"
port = 55456


try:
    if argv[1] == "-s":
        rutasocket = int(argv[2])
except:
    pass

nombrehost = socket.gethostname()
host = (socket.gethostbyname_ex(nombrehost))[-1][-1]

odiomivida = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("iniciando servidor\nport = {}\nhost = {}".format(port, host))

odiomivida.bind((host, port))

odiomivida.listen()

while True:
    coneccion, dir_cliente = odiomivida.accept()
    _thread.start_new_thread(asistir_cliente, (coneccion, dir_cliente))















