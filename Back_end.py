# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 11:19:11 2022

@author: Juan
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
            
    L_paq = L_cab + int(TABLA[posicion_codec][4])
    BWLL = L_paq*int(TABLA[posicion_codec][6])*8
    
    BW_st = Nlineas*BWLL* (1 + BWres/100)
    
    if (BW_st <= BW_cliente):
        cumple = True
    else:
        cumple = False
        
    return(BW_st, cumple)
    
    
def Envio_correo_informe(entradas, salidas, entradas_cte, salidas_cte): 
    
    salidas = salidas.split("-")
    port = 587
    smtp_server = "correo.ugr.es"
    sender_email = ""
    receiver_email = entradas[12]

    #password = 


    #Mensaje

    message = """\
    From: Empresa@correo.ugr.es
    TO: """ + receiver_email + """\ 
    Subject: Informe Final 

    **************************************************************

        
    - MOS: 


    """
     
       
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.close()