# Programa Servidor

import socket
import Back_end

datos_vector=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
resultado=""
# Se crea el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto, donde debemos indicar el servidor y puerto
server_address = ('localhost', 10800) #Si lo queremos hacer en ordenadores diferentes se debe dejar vacio, solo el puerto.
print('Comunicación {}  en el puerto {}'.format(*server_address))
sock.bind(server_address)

# Escuchando conexiones entrantes
sock.listen()

while True:
    # Esperando conexion
    print ('Esperando para conectarse')
    connection, client_address = sock.accept()
    try:
        print ('conectado')

        # Recibe los datos en trozos y reetransmite
        
        message = connection.recv(1024)
        print ('recibido "%s"' % message)
        print('Se recibe: '+ message.decode('utf-8'))

        message=message.decode('utf-8').split("-")
        i=int(message[0])
        data=message[1]
        datos_vector[i]=float(data)



         #--------------------MOS--------------------------
        if(i==0):

            MOS_elegido, codec_elegido, posicion_codec=Back_end.eleccion_codec(datos_vector[0])
            print ('El codec elegido es:'+codec_elegido)
            
            resultado=str(MOS_elegido)+ "-"+str(codec_elegido)+"-"
          
        #Enviar al final datos como string separados por guiones cada dato, para luego separar en cliente
        if(i==3):
            ret_calculado, cumple=Back_end.calculo_retardo(posicion_codec,datos_vector[1],datos_vector[2],datos_vector[3])
            resultado=resultado+str(ret_calculado)+"-"+str(cumple)+"-"

        if(i==7):
            Nlineas=Back_end.Calculo_lineas_BHT(datos_vector[4],datos_vector[5],datos_vector[6],datos_vector[7])
            resultado=resultado+str(Nlineas)+"-"

        if(i==11):
            BW_st, cumple=Back_end.Calculo_BWst(Nlineas,posicion_codec,datos_vector[8],datos_vector[9],datos_vector[10],datos_vector[11])
            resultado=resultado+str(BW_st)+"-"+str(cumple)+"-"
            connection.sendall(resultado.encode('ascii'))

    finally:
        # Cerrando conexion
        connection.close()