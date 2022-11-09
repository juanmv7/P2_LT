# Programa Cliente

import socket
import sys

message ='Vacio'
# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('150.214.205.73', 8750)
print ('conectando a %s puerto %s' % server_address, file=sys.stderr)
sock.connect(server_address)


try:
    
    while message!='salir':
         # Enviando datos
        print("El mensaje es: ")
        message = input().encode()

        print ('Enviando "%s"' % message, file=sys.stderr)
        sock.sendall(message)

        # Buscando respuesta
        amount_received = 0
        amount_expected = len(message)
    
        while amount_received < amount_expected:
            data = sock.recv(19)
            amount_received += len(data)
            print ('recibiendo "%s"' % data, file=sys.stderr)
    print('cerrando socket', file=sys.stderr)
    sock.close()    

finally:
    print ('cerrando socket', file=sys.stderr)
    sock.close()