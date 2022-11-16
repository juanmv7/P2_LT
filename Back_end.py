# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 11:19:11 2022

@author: Juan Muñoz
"""
import numpy as np
import smtplib
from math import factorial


codec_name = ["CBR (Kbps)", "CSS (Bytes)", "CSI (ms)", "MOS", "VPS (Bytes)", "VPS (ms)", "PPS", "RETARDO ALG (ms)"]
G711 = ["64", "80", "10", "4.1", "160", "20", "50", "0"]
G729 = ["8", "10", "10", "3.92", "20", "20", "50", "5"]
G723_1_63 = ["6.3", "24", "30", "3.9", "24", "30", "33.3", "7.5"]
G723_1_53 = ["5.3", "20", "30", "3.8", "20", "30", "33.3", "7.5"]
G726_32 = ["32", "20", "5", "3.85", "80", "20", "50", "0"]
G726_24 = ["24", "15", "5", "0", "60", "20", "50", "0"]
G728 = ["16", "10", "5", "3.61", "60", "30", "33.3", "0"]
G722_64 = ["64", "80", "10", "4.13", "160", "20", "50", "0"]
ilbc_mode_20 = ["15.2", "38", "20", "0", "38", "20", "50", "0"]
ilbc_mode_30 = ["13.33", "50", "30", "0", "50", "30", "33.3", "0"]

TABLA = [G711, G729, G723_1_63, G723_1_53, G726_32, G726_24, G728, G722_64, ilbc_mode_20, ilbc_mode_30]
TABLA_NAMES = ["G711", "G729", "G723_1_63", "G723_1_53", "G726_32", "G726_24", "G728", "G722_64", "ilbc_mode_20", "ilbc_mode_30"]

# Paso 1. Elección de codec a partir de MOS.

# @brief Esta funcion elige un Codec en funcion del MOS introducido
# 
# @param[in]  MOS             MOS que se requiere
# @param[out] MOS_elegido     MOS del codec elegido
# @param[out] codec_elegido   Codec elegido
# @param[out] posicion_codec  Posicion del codec en TABLA
##
def eleccion_codec(MOS):
    
    MOSes=[]
    for j in range(0,len(TABLA)-1):
        MOSes.append(float(TABLA[j][3]))
    
    MOS_elegido = max(MOSes)
    
    for j in range(0,len(TABLA)-1):
        if ((float(TABLA[j][3])>=MOS)&(float(TABLA[j][3])<MOS_elegido)):
            MOS_elegido = float(TABLA[j][3])


    for j in range(0,len(TABLA)-1):
        if str(MOS_elegido) in TABLA[j]:
            codec_elegido = TABLA_NAMES[j]

    posicion_codec =  TABLA_NAMES.index(codec_elegido)
    return (MOS_elegido, codec_elegido, posicion_codec)

# Paso 3. 


# @brief Esta funcion calcula el retaro de un CODEC en específico e 
#indica si este retardo cumple o no con el retardo requerido
# 
# @param[in]  posicion_codec  Posicion del codec en TABLA
# @param[in]  retardo_red     Retardo de la red
# @param[in]  jitter          jitter
# @param[in]  retardo_pedido  retardo requerido por el cliente
# @param[out] ret_calculado   retardo calculado con los parámetros de entrada
# @param[out] cumple          condición que indica si cumple o no con el retardo requerido
#
#
##
def calculo_retardo(posicion_codec, retardo_pedido, retardo_red, jitter):
    
    origen = float(TABLA[posicion_codec][5]) + float(TABLA[posicion_codec][7])
    destino = 0.1*float(TABLA[posicion_codec][5]) + jitter*np.arange(1.50, 2.1, 0.50) 
    
    ret_total = origen + retardo_red + destino
    
    if ret_total[1]<=retardo_pedido:
        ret_calculado = ret_total[1]   #Buffer x2
        cumple=True
    elif ret_total[0]<=retardo_pedido:
        ret_calculado = ret_total[0]   #Buffer x1.5
        cumple=True
    else:
        ret_calculado = ret_total[0]
        cumple=False
        
    return (ret_calculado, cumple)



# @brief   Esta funcion calcula la probabilidad de bloqueo frente a los recursos 
#          (lineas) y los Erlangs.
# 
# @param[in]  A             Erlangs
# @param[in]  m             Número de lineas 
# @param[out] Pb            Probabilidad de bloqueo
#
##   
def erlang(A, m):
    L = (A ** m) / factorial(m)
    sum_ = 0
    for n in range(m + 1): sum_ += (A ** n) / factorial(n)

    return (L / sum_)



# @brief Esta funcion calcula el numero de lineas necesarias a partir de la 
#        prob de bloqueo y el caso peor en la BHT.
# 
# @param[in]  Nc              Numero de clientes
# @param[in]  Nl              Numero de lineas por cliente
# @param[in]  Tpll            Tiempo medio por llamada (min)
# @param[in]  Pb              Probabilidad de bloqueo
# @param[out] Nlineas         Numero de lineas en base a los Erlangs y la P_bloqueo
#
##    
def Calculo_lineas_BHT(Nc, Nl, Tpll, Pb):
    
    BHT = (Nc*Nl*Tpll)/60
    Nlineas = 1
    for i in range(1,1000):
        Nlineas+=i                               #Nlineas = Nlineas + i
        if (erlang(int(BHT), Nlineas) <= Pb):
            break
    
    return(Nlineas)
    
# @brief Esta funcion calcula el ancho de banda necesario para cursar Nlineas llamadas
#        a partir del tipo de encapsulacion y del uso de cRTP o no. Además compara
#        con el BW introducido por el cliente y si cumple o no con este.
# 
# @param[in]  Nlineas              Numero de llamadas
# @param[in]  posicion_codec       Posicion del codec en TABLA
# @param[in]  BWres                Ancho de banda de reserva (en porcentaje)
# @param[in]  BW_cliente           Ancho de banda introducido por el cliente
# @param[in]  encapsulacion        Tipo de encapsulacion de los paquetes 
#                                       - Ethernet: 1
#                                       - Ethernet 802.1q: 2
#                                       - Ethernet q-in-q: 3
#                                       - PPPOE: 4
#                                       - PPPOE 802.1q: 5
# @param[in]  bool_cRTP            Indica si se va a hacer compresión RTP
# @param[out] BW_st                Ancho de banda resultante
# @param[out] Cumple                Indica si el ancho de banda cumple con el introducido por el cliente
##     
def Calculo_BWst(Nlineas, posicion_codec, BWres, BW_cliente, bool_cRTP, encapsulacion):
    
    
    if (encapsulacion==1):
        if (bool_cRTP):
            L_cab = 4 + 18
        else: 
            L_cab = 40 + 18
    elif (encapsulacion==2):
        if (bool_cRTP):
            L_cab = 4 + 22
        else:
            L_cab = 40 + 22
    elif (encapsulacion==3):
        if (bool_cRTP):
            L_cab = 4 + 26
        else:
            L_cab = 40 + 26
    elif (encapsulacion==4):
        if (bool_cRTP):
            L_cab = 4 + 26
        else: 
            L_cab = 40 + 26
    elif (encapsulacion==5):
        if (bool_cRTP):
            L_cab = 4 + 30
        else: 
            L_cab = 40 + 30
            
    L_paq = L_cab + float(TABLA[posicion_codec][4])
    BWLL = L_paq*float(TABLA[posicion_codec][6])*8
    
    BW_st = Nlineas*BWLL* (1 + BWres/100)
    
    if (BW_st <= BW_cliente):
        cumple = True
    else:
        cumple = False
        
    return(BW_st, cumple)
    
  
def Envio_correo_informe(entradas, salidas, entradas_cte, salidas_cte): 
    
#"Introduzca el valor deseado del MOS:"0
#"Introduzca el retardo requerido (ms):"#1
#"Introduzca el retardo de red (ms):"#2
#"Introduzca el jitter total (ms):"#3
#"Introduzca el número de clientes (Nc):"#4
#"Introduzca el numero de líneas \n por cliente (Nl):"#5
#"Introduzca el tiempo medio por \n llamada (Tpll)(Min):"#6
#"Introduzca la probabilidad \n de bloqueo (%):"#7
#"Introduzca el ancho de banda \n de reserva (%):"#8
#"Introduzca el ancho de banda \n requerido (bps):"#9
#"Indica si desea compresion cRTP  \n (Yes=1 No=0):"#10
#"Introduzca el tipo de encapsulación:"]#11##

    port = 587
    smtp_server = "correo.ugr.es"
    sender_email = "pablorofu@correo.ugr.es"
    receiver_email = entradas[12]
    password="teleco4"


    j=0
    k=0
    #inicializamos vectores
    MOS=[]
    retardo=[]
    retardo_red=[]
    jitter=[]
    nc=[]
    nl=[]
    tpll=[]
    pb=[]
    banda_requerido=[]
    banda_reserva=[]
    cRTP=[]
    encapsulacion=[]
    entradas_sin_cabecera=[]
    entradas_sin_guiones=[]
    cabeceras_de_entradas=[]
    
    
    
    #le quitamos los guiones a la lista entradas_cte
    for z in range(0,len(entradas_cte)):#NO HACE FALTA PONER -1, YA LO HACE RANGE
        entradas_sin_guiones.append(entradas_cte[z].split("-"))
    #una vez quitamos los guiones tenemos una lista en la que cada componente es una lista
    for j in range(0,len(entradas_sin_guiones)):
        cabeceras_de_entradas.append(entradas_sin_guiones[j][0]) #recorremos las diferentes componentes de la lista entradas_sin_guiones y en cada componente hay 2 componentes que son la cabecera y el contenido del mensaje
        entradas_sin_cabecera.append(entradas_sin_guiones[j][1])
    for k in range(0,len(cabeceras_de_entradas)):#identificamos las cabeceras para saber de qué mensaje se trata
        if(cabeceras_de_entradas[k]=='0'):
            MOS.append(entradas_sin_cabecera[k]) #introduce entradas_sin_cabecera[k] en la siguiente posición de MOS
        elif(cabeceras_de_entradas[k]=='1'):
            retardo.append(entradas_sin_cabecera[k])
        elif(cabeceras_de_entradas[k]=='2'):
            retardo_red.append(entradas_sin_cabecera[k])
        elif(cabeceras_de_entradas[k]=='3'):
            jitter.append(entradas_sin_cabecera[k])
        elif(cabeceras_de_entradas[k]=='4'):
            nc.append(entradas_sin_cabecera[k])
        elif(cabeceras_de_entradas[k]=='5'):
            nl.append(entradas_sin_cabecera[k])
        elif(cabeceras_de_entradas[k]=='6'):
            tpll.append(entradas_sin_cabecera[k])
        elif(cabeceras_de_entradas[k]=='7'):
            pb.append(entradas_sin_cabecera[k])
        elif(cabeceras_de_entradas[k]=='8'):
            banda_reserva.append(entradas_sin_cabecera[k])
        elif(cabeceras_de_entradas[k]=='9'):
            banda_requerido.append(entradas_sin_cabecera[k])
        elif(cabeceras_de_entradas[k]=='10'):#cRTP
            if(entradas_sin_cabecera[k]=='True'):
                cRTP.append('con cRTP')
            else:
                cRTP.append('sin cRTP')
        elif(cabeceras_de_entradas[k]=='11'):#encapsulacion
            if(entradas_sin_cabecera[k]=='1'):
                encapsulacion.append('Ethernet')
            elif(entradas_sin_cabecera[k]=='2'):
                encapsulacion.append('Ethernet 802.1q')
            elif(entradas_sin_cabecera[k]=='3'):
                encapsulacion.append('Ethernet q-in-q')
            elif(entradas_sin_cabecera[k]=='4'):
                encapsulacion.append('PPPOE')
            elif(entradas_sin_cabecera[k]=='5'):
                encapsulacion.append('PPPOE 802.1q')

    """for i in range(0,len(MOS)): 
        MOS[i]=int(MOS[i]) #pasamos de una lista en la que cada componente es un str a una lista en la que cada componente es un int
    MOS=str(MOS) #luego pasamos de lista a str"""
    
    #tenemos una lista cuyas componentes son listas, cada componente de cada lista se va a transformar a enteros, y una vez tenemos una lista con enteros, transformamos la lista de enteros en un str de enteros porque el mensaje solo admite str
    vector=[MOS,retardo,retardo_red,jitter,nc,nl,tpll,pb,banda_reserva,banda_requerido]
    for i in range(0,len(vector)):
        for j in range(0,len(vector[i])):
            vector[i][j]=float(vector[i][j])
        vector[i]=str(vector[i])
    
    MOS_elegido=[]
    codec_elegido=[]
    ret_calculado=[]
    cumple_ret=[]
    Nlineas=[]
    Bw_st=[]
    cumple_Bw=[]
    salidas_sin_guiones=[]
    cabeceras_de_salidas=[]
    salidas_sin_cabecera=[]
    
        
    
    for z in range(0,len(salidas_cte)):#NO HACE FALTA PONER -1, YA LO HACE RANGE
        salidas_sin_guiones.append(salidas_cte[z].split("-"))
    for j in range(0,len(salidas_sin_guiones)):
        cabeceras_de_salidas.append(salidas_sin_guiones[j][0])
        salidas_sin_cabecera.append(salidas_sin_guiones[j][1])
    for k in range(0,len(cabeceras_de_salidas)):
        if(cabeceras_de_salidas[k]=='0'):
            MOS_elegido.append(salidas_sin_cabecera[k]) #introduce entradas_sin_cabecera[k] en la siguiente posición de MOS
        elif(cabeceras_de_salidas[k]=='1'):
            codec_elegido.append(salidas_sin_cabecera[k])
        elif(cabeceras_de_salidas[k]=='2'):
            ret_calculado.append(salidas_sin_cabecera[k])
        elif(cabeceras_de_salidas[k]=='3'):
            if(salidas_sin_cabecera[k]=='True'):
                cumple_ret.append('cumple con el retardo')
            else:
                cumple_ret.append('no cumple con el retardo')
        elif(cabeceras_de_salidas[k]=='4'):
            Nlineas.append(salidas_sin_cabecera[k])
        elif(cabeceras_de_salidas[k]=='5'):
            Bw_st.append(salidas_sin_cabecera[k])
        elif(cabeceras_de_salidas[k]=='6'):
            if(salidas_sin_cabecera[k]=='True'):
                cumple_Bw.append('cumple con el ancho')
            else:
                cumple_Bw.append('no cumple con el ancho')
            
    vector2=[MOS_elegido,ret_calculado,Nlineas,Bw_st]
    for i in range(0,len(vector2)):
        for j in range(0,len(vector2[i])):
            vector2[i][j]=float(vector2[i][j])
        vector2[i]=str(vector2[i])


#- Ethernet --> 1\n  
#- Ethernet 802.1q --> 2\n  
#- Ethernet q-in-q --> 3\n  
#- PPPOE: --> 4\n  
#- PPPOE 802.1q: --> 5"]

    #Mensaje

    message = """
    
    From: Empresa@correo.ugr.es
    TO: """ + receiver_email + """
    Subject: Informe Final 
    
    
    
    **************************************************************
    
    AQUI TENEMOS LOS DATOS QUE USTED HA INTRODUCIDO:
    
    MOS: """+vector[0]+"""
    RETARDO REQUERIDO: """+vector[1]+""" ms
    RETARDO DE RED: """+vector[2]+""" ms
    JITTER: """+vector[3]+"""" ms
    NUMERO DE CLIENTES: """+vector[4]+""" clientes
    NUMERO DE LINEAS POR CLIENTE: """+vector[5]+""" lineas
    TIEMPO MEDIO POR LLAMADA: """+vector[6]+""" mins
    PROB. DE BLOQUEO: """+vector[7]+""" porcentaje
    ANCHO DE BANDA DE RESERVA: """+vector[8]+""" porcentaje
    ANCHO DE BANDA REQUERIDO: """+vector[9]+""" bps
    COMPRESION cRTP: """+str(cRTP)+"""
    TIPO DE ENCAPSULACION: """+str(encapsulacion)+"""
    
    AQUI ESTAN LAS DIFERENTES SALIDAS QUE HEMOS OBTENIDO:
        
    MOS ELEGIDO: """ +vector2[0]+ """
    CODEC ELEGIDO: """ +str(codec_elegido)+ """
    RETARDO CALCULADO: """ +vector2[1]+ """ ms
    CUMPLE RETARDO: """ +str(cumple_ret)+ """
    NUMERO DE LINEAS FINALES: """ +vector2[2]+ """ lineas
    ANCHO DE BANDA CALCULADO: """ +vector2[3]+ """ bps
    CUMPLE ANCHO DE BANDA: """ +str(cumple_Bw)+ """
                

    **************************************************************
    
    LOS DATOS FINALES QUE HEMOS UTILIZADO PARA LOS CALCULOS SON:
        
    MOS: """+str(MOS[len(MOS)-1])+"""
    RETARDO REQUERIDO: """+str(retardo[len(retardo)-1])+""" ms
    RETARDO DE RED: """+str(retardo_red[len(retardo_red)-1])+""" ms
    JITTER: """+str(jitter[len(jitter)-1])+""" ms
    NUMERO DE CLIENTES: """+str(nc[len(nc)-1])+""" clientes
    NUMERO DE LINEAS POR CLIENTE: """+str(nl[len(nl)-1])+"""
    TIEMPO MEDIO POR LLAMADA: """+str(tpll[len(tpll)-1])+""" mins
    PROB. DE BLOQUEO: """+str(pb[len(pb)-1])+""" porcentaje
    ANCHO DE BANDA DE RESERVA: """+str(banda_reserva[len(banda_reserva)-1])+""" porcentaje
    ANCHO DE BANDA REQUERIDO: """+str(banda_requerido[len(banda_requerido)-1])+""" bps
    COMPRESION cRTP: """+str(cRTP[len(cRTP)-1])+"""
    TIPO DE ENCAPSULACION: """+str(encapsulacion[len(encapsulacion)-1])+"""
  
    LAS SALIDAS FINALES SON:

    MOS ELEGIDO: """ +str(MOS_elegido[len(MOS_elegido)-1])+ """
    CODEC ELEGIDO: """ +str(codec_elegido[len(codec_elegido)-1])+ """
    RETARDO CALCULADO: """ +str(ret_calculado[len(ret_calculado)-1])+ """ ms
    CUMPLE RETARDO: """ +str(cumple_ret[len(cumple_ret)-1])+ """
    NUMERO LINEAS FINALES: """ +str(Nlineas[len(Nlineas)-1])+ """ lineas
    ANCHO DE BANDA CALCULADO: """ +str(Bw_st[len(Bw_st)-1])+ """ bps
    CUMPLE ANCHO DE BANDA: """ +str(cumple_Bw[len(cumple_Bw)-1])+ """
    
    **************************************************************
      
    """ 

    print(message)

    with smtplib.SMTP(smtp_server,port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email,password)
        server.sendmail(sender_email,receiver_email,message)
        server.close()