# Programa Servidor

import socket
import sys

# Se crea el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto, donde debemos indicar el servidor y puerto

server_address = ('localhost', 10094) #Si lo queremos hacer en ordenadores diferentes se debe dejar vacio, solo el puerto.
print('Comunicación {}  en el puerto {}'.format(*server_address))
sock.bind(server_address)

# Escuchando conexiones entrantes
sock.listen(1)

while True:
    # Esperando conexion
    print ('Esperando al cliente para conectarse', file=sys.stderr)
    connection, client_address = sock.accept()

    try:
        print ('Conexion desde el cliente', client_address, file=sys.stderr)

        # Comprueba que se han recibido los datos, y reenvia respuesta
        while True:
            data = connection.recv(1024) #Llega el mensaje
            data2=float(data)
            print ('Se ha recibido el mensaje "%s"' % data, file=sys.stderr)
            
            if data:
                print ('Se ha enviado mensaje de vuelta al cliente', file=sys.stderr)
                connection.sendall(data)
                if data2==4: #Compara mensaje que nos llega en este caso el MOS
                    print ('funciona')
            else:
                 print ('No hay mas datos', client_address, file=sys.stderr)
            break
            
    finally:
        # Cerrando conexion
        connection.close()
