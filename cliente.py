#cliente
import socket
import sys

argv = list(sys.argv)
rutasocket = "/tmp/db.tuples.sock"
port = 55456

try:
    if argv[1] == "-s":
        rutasocket = argv[2]
except:
    pass



host = input("ip del servidor: ")
quierollorar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
superf = False

cmd = ""
conectado = False
while cmd != quit:
    cmd = input("=>")
    comando = cmd.split('(')[0]


    if comando == 'connect':
        if conectado:
            print("ya estas conectado")
        else:
            try:
                quierollorar.connect((host, port))
                conectado = True
                print("conectado exitosamente! ")
            except:
                print("ERROR: error al conectar,asegurese de que ingreso bien la ip")
                host = input('reingrese la ip: ')
                print("vuelva a conectarse")
    elif comando == 'quit':
        if conectado:
            quierollorar.send('0/@quit'.encode())
        print("cerrando sesion\n")
        conectado = False
        break
    elif comando == 'disconnect':
        if conectado:
            quierollorar.send('0/@disconnect'.encode())
            conectado = False
            quierollorar.close()
            print("se ha desconectado correctamente")
        else:
            print("ERROR: aun no estas conectado a nada")

    elif conectado:

        if comando=='update':
            try:
                key = cmd.split('(')[1].split(',')[0]
                value = cmd.split('(')[1].split(',')[1:]
                val = ''
                for i in value:
                        val += i
                try:
                    key = int(key)
                    quierollorar.send('2/@update/@{}/@{}'.format(key,val).encode())
                    print(quierollorar.recv(4096).decode())

                except:
                    print("ERROR: la llave debe ser un entero")
            except:
                print('parametros incorrectos')

        elif comando == 'insert':
            try:
                if len(cmd.split('(')[1].split(',')) > 1:
                    value = cmd.split('(')[1].split(',')[1:]
                    val = ''
                    key= cmd.split('(')[1].split(',')[0]
                    for i in value:
                        val += i
                    try:
                        print('llegue')
                        key = int(key)
                        print("lo logre")
                        quierollorar.send('2/@insert/@{}/@{}'.format(key,val).encode())
                        print(quierollorar.recv(4096).decode())
                    except:
                        print("ERROR: la llave debe ser un entero")
                            
                else:
                    value = cmd.split('(')[1].replace(')', '')
                    quierollorar.send('1/@{}/@{}'.format(comando, value).encode())
                    responce_key = quierollorar.recv(4096).decode()
                    print("se ha guardado con exito en la llave {}".format(responce_key))
            except:
                print('parametros incorrectos')
            
        elif comando == 'get':
            try:
                key = cmd.split('(')[1].replace(')', '')
                try:
                    int(key)
                    quierollorar.send('1/@get/@{}'.format(key).encode())
                    valor = quierollorar.recv(4096).decode()
                    print("{}".format(valor))    
                except:
                    print('ERROR: los valores de key deben ser enteros')
            except:
                print('parametros incorrectos')
        elif comando == 'peek':
            try:
                key = cmd.split('(')[1].replace(')', '')
                try:
                    int(key)
                    quierollorar.send('1/@{}/@{}'.format(comando, key).encode())
                    response = quierollorar.recv(4096).decode()
                    print(response)
                except:
                    print('ERROR: los valores de key deben ser enteros')
            except:
                print('parametros incorrectos')
            
        elif comando == 'delete':
            try:
                key = cmd.split('(')[1].replace(')', '')
                try:
                    int(key)
                    quierollorar.send('1/@{}/@{}'.format(comando, key).encode())
                    response = quierollorar.recv(4096).decode()
                    print(response)
                except:
                    print('ERROR: los valores de key deben ser enteros')
            except:
                print('parametros incorrectos')                
        elif comando == 'list':
            quierollorar.send('0/@list'.encode())
            print(quierollorar.recv(4096).decode())
        
            
        else:
            print("comando inexistente")
            
            
    else:
        print("ERROR: comando inexistente o falta conexion para realiazar comando")























