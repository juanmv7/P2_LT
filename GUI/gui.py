# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import *

#VARIABLES GLOBALES
i=0 #para iterar entre frames
frames=[] #vector donde guardaremos los distintos frames o paginas del programa
valores=[]
cuadroTexto=[]
mensaje=["Introduzca el MOS", "Introduzca el retardo requerido (ms)", "Introduzca el retardo de red (ms)", "Introduzca el jitter total (ms)","Introduzca el numero de clientes (Nc)" ,"Introduzca el numero de lineas por cliente (Nl)", "Introduzca el tiempo medio por llamada (Tpll)" ,"Introduzca la probabilidad de bloqueo (%)","Introduzca el ancho de banda de reserva (%)" ,"Introduzca el ancho de banda requerido (bps)", "Indica si quiere compresion cRTP o no"]
#FALTAN MENSAJES: tipos de encapsulacion

#Crear y avanzar frame sera lo mismo. Esto implica que cada vez que volvamos atras, debemos volver a rellenar (y por tanto reecribir) el frame
def crear_frame():
    global frames
    frames.append(tk.Frame(root, width=600, height=400))

#Al retroceder no se modifica el frame, pero luego al volver al avanzar si que tendremos que reescribirlo!
def retroceder_pagina():
    global i, frames, valores
    valores.pop()
    frames[i].forget()# dejamos de visualizar este frame
    i=i-1 #iteramos
    frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame

def crear_boton(k):
    botonEnviar=tk.Button(frames[k], text="Enviar", command=codigoBoton)
    botonEnviar.place(x=250,y=50)
    botonAtras=tk.Button(frames[k], text="Atras", command=retroceder_pagina)
    botonAtras.place(x=330,y=50)

def crear_etiqueta(k):
    global mensaje
    miLabel=tk.Label(frames[k], text=mensaje[k], fg="blue")
    miLabel.place(x=240,y=10)
    
def crear_entry(k):
    global cuadroTexto
    cuadroTexto.append(tk.Entry(frames[k]))#NO SE ESTA ACTUALIZANDO VALOR
    cuadroTexto[k].place(x=250,y=30)
    
def codigoBoton():
     global i, frames, valores
     valores.append(cuadroTexto[i].get())
     frames[i].forget()
     i=i+1
     frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame
     
     
########## CREACION VENTANA RAIZ #############

root=tk.Tk() #creamos una varibale de instancia de la clase tk. Crea la ventana principal e inicia interpetre Tcl/Tk
root.title("VoIP Network Designer") #titulo ventana
root.config(width=600, height=400) #dimensiones ventana

for k in range(0,13,1):
    crear_frame()

########## FRAME 0 ##########
frames[0].pack(fill='both', expand=1) #mostramos el primer frame. Las proximas se mostraran con codigo boton

crear_boton(0)
crear_etiqueta(0)
crear_entry(0)


####### FRAME 1 ######
crear_boton(1)
crear_etiqueta(1)
crear_entry(1)

####### FRAME 2 ######
crear_boton(2)
crear_etiqueta(2)
crear_entry(2)

####### FRAME 3 ######
crear_boton(3)
crear_etiqueta(3)
crear_entry(3)

####### FRAME 4 ######
crear_boton(4)
crear_etiqueta(4)
crear_entry(4)

####### FRAME 5 ######
crear_boton(5)
crear_etiqueta(5)
crear_entry(5)

####### FRAME 6 ######
crear_boton(6)
crear_etiqueta(6)
crear_entry(6)

####### FRAME 7 ######
crear_boton(7)
crear_etiqueta(7)
crear_entry(7)

####### FRAME 8 ######
crear_boton(8)
crear_etiqueta(8)
crear_entry(8)

####### FRAME 9 ######
crear_boton(9)
crear_etiqueta(9)
crear_entry(9)




# MAIN LOOP (FINAL)

root.mainloop() #Este metodo 'dibuja' la ventana constantemente. Debera estar al final