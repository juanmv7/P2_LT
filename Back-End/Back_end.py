# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 11:19:11 2022

@author: Juan
"""
import numpy as np


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
    
    MOS_elegido = 5
    for j in range(0,len(TABLA)-1):
        if ((float(TABLA[j][3])>MOS)&(float(TABLA[j][3])<MOS_elegido)):
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
def calculo_retardo(posicion_codec, retardo_red, jitter, retardo_pedido):
    
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

# @brief Esta funcion calcula el numero de lineas necesarias a partir de la 
#        prob de bloqueo y el caso peor en la BHT.
# 
# @param[in]  Nc              Numero de clientes
# @param[in]  Nl              Numero de lineas por cliente
# @param[in]  Tpll            Tiempo medio por llamada
# @param[in]  Pb              Probabilidad de bloqueo
#
#
##    
def Calculo_lineas_BHT(Nc, Nl, Tpll, Pb):
    
    BHT = (Nc*Nl*Tpll)/60
    
    