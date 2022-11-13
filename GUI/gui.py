# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import *
import Back_end

#VARIABLES GLOBALES
i=0 #para iterar entre frames
frames=[] #vector donde guardaremos los distintos frames o paginas del programa
MOS_elegido=-1
codec_elegido='0'
posicion_codec=-1
valor=0.0

#Crear y avanzar frame sera lo mismo. Esto implica que cada vez que volvamos atras, debemos volver a rellenar (y por tanto reecribir) el frame
def crear_frame():
    global i
    global frames
    frames[i].forget()
    i=i+1
    frames.append(tk.Frame(root, width=600, height=400))
    frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame

#Al retroceder no se modifica el frame, pero luego al volver al avanzar si que tendremos que reescribirlo!
def retroceder_pagina():
    global i
    global frames
    frames[i].forget()# dejamos de visualizar este frame
    i=i-1 #iteramos
    frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame

def crear_boton():
    botonEnviar=tk.Button(frames[i], text="Enviar", command=codigoBoton)
    botonEnviar.place(x=250,y=50)
    botonAtras=tk.Button(frames[i], text="Atras", command=retroceder_pagina)
    botonAtras.place(x=330,y=50)

def crear_etiqueta(mensaje):
    miLabel=tk.Label(frames[i], text=mensaje, fg="blue")
    miLabel.place(x=240,y=10)
    
def crear_entry():
    global valor
    cuadroTexto=tk.Entry(frames[i],textvariable=valor)#NO SE ESTA ACTUALIZANDO VALOR
    cuadroTexto.place(x=250,y=30)
    
    
def codigoBoton():
   global MOS_elegido, codec_elegido, posicion_codec, valor
   MOS_elegido, codec_elegido, posicion_codec= Back_end.eleccion_codec(valor)
   print("El valor es bueno")
   #cuadroTexto.delete(0,END) 
   crear_frame()
    
########## CREACION VENTANA RAIZ #############

root=tk.Tk() #creamos una varibale de instancia de la clase tk. Crea la ventana principal e inicia interpetre Tcl/Tk
root.title("VoIP Network Designer") #titulo ventana
root.config(width=650, height=350) #dimensiones ventana


########## FRAME 0 ##########
frames.append(tk.Frame(root, width=600, height=400))
frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame

crear_boton()
crear_etiqueta("Introduzca el MOS")
crear_entry()

############ FRAME 2 #############







# MAIN LOOP (FINAL)

root.mainloop() #Este metodo 'dibuja' la ventana constantemente. Debera estar al final