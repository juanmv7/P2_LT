# Programa Servidor

import socket
import Back_end


datos_vector=[0,0,0,0,0,0,0,0,0,0,0,0,0] #datos_vector: Vector que inicializamos a cero, con 13 posicione, se llenará de los datos finales introducidos por el cliente
datos_vector_cte = [] #datos_vector_cte: Vector que se llenará de todos los datos introducidos por el cliente, será un registro.
resultado_cte = [] #resultado_cte: Vector con todos los resultados con los que pruebe el cliente.
resultado="" #resultado: Resultado final calculado a a partir de los datos finales.


# Se crea el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto, donde debemos indicar el servidor y puerto
server_address = ('localhost', 10800) 
print('Comunicación {}  en el puerto {}'.format(*server_address)) 
sock.bind(server_address)

# Escuchando conexiones entrantes
sock.listen()


while True:
    # Esperando conexión
    print ('Esperando para conectarse') #Mensaje que nos indica en el terminal que está esperando comunicación
    connection, client_address = sock.accept()
    try:
        print ('Conectado')
        message = connection.recv(1024)
        print ('recibido "%s"' % message)
        print('Se recibe: '+ message.decode('utf-8'))
        
        # Recibimos los datos y separamos cabecera de datos para introducirlo en el
        # vector correspondiente. Tenemos el vector datos_vector que en cada posición de i
        # guarda un valor. i nos indica que tipo de dato es y esa es la cabecera que hemos pasado
        # Importante: i depende del frame en el que estemos y al estar cada dato asociado a un frame,
        # eso hace que i esté asociado a un tipo de dato. Consultar README para más información.
        
        datos_vector_cte.append(message.decode('utf-8'))
        message=message.decode('utf-8').split("-")
        
        i=int(message[0])
        data=message[1]

        # Tenemos que pasar los datos a floar (general) ya que vienen en forma de str. El 12 es el correo así que NO.
        if (i<12):
            datos_vector[i]=float(data)

         #--------------------MOS--------------------------
         #Calculamos el MOS, el codec elegido  haciendo uso de la funcion eleccion_codec perteneciente al Back_End 
         #Introducimos las salida final en un string, separandolas por guiones, así como el registro de todas las soluciones en un vector
        
        if(i==0):
            MOS_elegido, codec_elegido, posicion_codec=Back_end.eleccion_codec(datos_vector[0])
            print ('El codec elegido es:'+codec_elegido)
            resultado=str(MOS_elegido)+ "-"+str(codec_elegido)+"-"
            
            resultado_cte.append("0-"+str(MOS_elegido))
            resultado_cte.append("1-"+str(codec_elegido))
            
        
        #--------------------Retardo--------------------------
        #Calculamos el retardo haciendo uso de la funcion calculo_retardo perteneciente al Back_End 
        
        if(i==3):
            ret_calculado, cumple=Back_end.calculo_retardo(posicion_codec,datos_vector[1],datos_vector[2],datos_vector[3])
            resultado=resultado+str(ret_calculado)+"-"+str(cumple)+"-"
            
            resultado_cte.append("2-"+str(ret_calculado))
            resultado_cte.append("3-"+str(cumple))

        #--------------------Nlineas--------------------------
        #Calculamos el número de líneas haciendo uso de la funcion Calculo_lineas_BHT perteneciente al Back_End 
        
        if(i==7):
            Nlineas=Back_end.Calculo_lineas_BHT(datos_vector[4],datos_vector[5],datos_vector[6],datos_vector[7]/100)
            resultado=resultado+str(Nlineas)+"-"
            
            resultado_cte.append("4-"+str(Nlineas))

        #--------------------BW_St--------------------------
        #Calculamos el ancho de banda resultante haciendo uso de la funcion Calculo_BWst perteneciente al Back_End, 
        #Enviamos el resultado con las salidas finales para crear el informe al cliente

        if(i==11):
            BW_st, cumple=Back_end.Calculo_BWst(Nlineas,posicion_codec,datos_vector[8],datos_vector[9],int(datos_vector[10]),int(datos_vector[11]))
           
            resultado=resultado+str(BW_st)+"-"+str(cumple)

            connection.sendall(resultado.encode('ascii'))
            
            resultado_cte.append("5-"+str(BW_st))
            resultado_cte.append("6-"+str(cumple))
            
        #--------------------Envio_correo--------------------------
        #Añadimos  la dirección de correo al vector de datos y
        # y usamos la funcion Envio_correo_informe del Back_END
        
        # Hasta ahora no se ha mencionado datos_vector_cte y resultado_cte. Son 
        # 2 vectores que contienen todos las entradas del cliente. Para resultados 
        # he añadido una cabecera similar a la de datos_vector con valores de X- 
        # que dependen del tipo de resultado. Consultar README para más información
    
        if(i==12):
            datos_vector[i]=data 

            Back_end.Envio_correo_informe(datos_vector, resultado, datos_vector_cte, resultado_cte)
            connection.close()
        
        
    finally:
        # Cerrando conexión entre servidor y cliente
        connection.close()