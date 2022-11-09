# Programa Cliente

import socket
import sys
import Grafico

message2 ='Vacio'
# Creando un socket TCP/IP
sock = socket.socket()

# Conecta el socket en el puerto cuando el servidor esté escuchando
<<<<<<< HEAD
server_address = ('150.214.205.73', 8750)
=======
server_address = ('localhost', 10094)
>>>>>>> 1d28b7aff1392cddfe8765a0b32e999271d4e020
print ('conectando a %s puerto %s' % server_address, file=sys.stderr)
sock.connect(server_address)



    
while message2!=48: #Numero que se puede cambiar
    # Enviando datos
    #print("El mensaje es: ")
    #message = input().encode('ascii')
    message=Grafico.MOS.encode
    message2=float(message)

    print ('Enviando "%s"' % message, file=sys.stderr)
    sock.send(message)

        # Buscando respuesta
        #amount_received = 0
        #amount_expected = len(message)
    
        #while amount_received < amount_expected:
         #data = sock.recv(1024)
         #amount_received += len(data)
         #print ('recibiendo "%s"' % data, file=sys.stderr)
        
print('cerrando socket', file=sys.stderr)
sock.close()    