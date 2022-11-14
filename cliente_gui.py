# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import *
#from PIL import ImageTk, Image
import socket

#VARIABLES GLOBALES
i=0 #para iterar entre frames
frames=[] #vector donde guardaremos los distintos frames o paginas del programa
valores=[]
cuadroTexto=[]
mensaje=["Introduzca el valor deseado del MOS:", "Introduzca el retardo requerido (ms):", "Introduzca el retardo de red (ms):", "Introduzca el jitter total (ms):","Introduzca el número de clientes (Nc):" ,"Introduzca el numero de líneas \n por cliente (Nl):", "Introduzca el tiempo medio \n por llamada (Tpll)(Min):" ,"Introduzca la probabilidad \n de bloqueo (%):","Introduzca el ancho de banda \n de reserva (%):" ,"Introduzca el ancho de banda \n requerido (bps):", "Indica si desea compresion cRTP  \n (Yes=1 No=0):","Introduzca el tipo de encapsulación:\n  - Ethernet --> 1\n  - Ethernet 802.1q --> 2\n  - Ethernet q-in-q --> 3\n  - PPPOE: --> 4\n  - PPPOE 802.1q: --> 5"]
#FALTAN MENSAJES: tipos de encapsulacion

#Crear y avanzar frame sera lo mismo. Esto implica que cada vez que volvamos atras, debemos volver a rellenar (y por tanto reecribir) el frame
def crear_frame():
    global frames
    frames.append(tk.Frame(root, width=400, height=200))

#Al retroceder no se modifica el frame, pero luego al volver al avanzar si que tendremos que reescribirlo!
def retroceder_pagina():
    global i, frames, valores
    valores.pop()
    frames[i].forget()# dejamos de visualizar este frame
    i=i-1 #iteramos
    frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame

def crear_boton(k):
    
    botonEnviar=tk.Button(frames[k], text="Enviar", command=codigoBoton,font=("Comic Sans",10),fg="black",activebackground="#90CAF9")
    botonEnviar.place(x=195,y=85)
    if(k>0):
        botonAtras=tk.Button(frames[k], text="Atras", command=retroceder_pagina,font=("Comic Sans",10),fg="black",activebackground="red")
        botonAtras.place(x=120,y=85)

def crear_etiqueta(k):
    global mensaje
    miLabel=tk.Label(frames[k], text=mensaje[k], fg="blue")
    miLabel.place(x=100,y=10)
    
def crear_entry(k):
    global cuadroTexto
    cuadroTexto.append(tk.Entry(frames[k]))
    cuadroTexto[k].place(x=120,y=60)
    
def codigoBoton():
    global i, frames, valores

    Mal=True

     
    valores.append(cuadroTexto[i].get())

    #  if(valores[i]!=''): #Control error con 0 y ""
    Conectar_server()
    frames[i].forget()
    i=i+1
    frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame
    #    Mal=False
        #Para crear ultimo frame
        #if(i==13):
        #crear ultimo frame
    #  else:
    #     #Para cuando no metes un valor no se rompa, ponga el valor 0, pero sale fallo en Back
    #      miLabel2=tk.Label(frames[i], text="Valor incorrecto,introduzca otro",font=("Comic Sans",12), fg="red")
    #      miLabel2.place(x=80,y=80)
    #      valores.append(cuadroTexto[i].get())
        


def Conectar_server():
    global i
    # Programa Cliente
    # Creando un socket TCP/IP
    sock = socket.socket()

    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = ('localhost', 10800)
    print ('conectando a %s puerto %s' % server_address)
    sock.connect(server_address)
    if(i<11):

        message=valores[i].encode('ascii')
        cabecera=(str(i)+'-')
        print ('Enviando "%s"' % message)
        sock.send(cabecera.encode('ascii')+ message) 
        sock.close()
    else:
        message=valores[i].encode('ascii')
        cabecera=(str(i)+'-')
        print ('Enviando "%s"' % message)
        sock.send(cabecera.encode('ascii')+ message) 
        data = sock.recv(1024)
        print('Recibiendo "%s"' % data)
        sock.close()

     
########## CREACION VENTANA RAIZ #############

root=tk.Tk() #creamos una varibale de instancia de la clase tk. Crea la ventana principal e inicia interpetre Tcl/Tk
root.title("VoIP Network Designer") #titulo ventana
root.config(width=600, height=200) #dimensiones ventana
root.iconbitmap("LT_Simbolo.ico")
root.resizable(0,0)


for k in range(0,14):
    crear_frame()

########## FRAME 0 ##########
frames[0].pack(fill='both', expand=1) #mostramos el primer frame. Las proximas se mostraran con codigo boton

crear_boton(0)
crear_etiqueta(0)
crear_entry(0)
#Añadir fotos
# image= Image.open("MOS_photo.png")
# image=image.resize((100,100), Image.ANTIALIAS)
# img =ImageTk.PhotoImage(image)
# img_final=tk.Label(frames[0], image=img)
# img_final.place(x=240,y=250)
# img_final.pack()

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

####### FRAME 10 ######
crear_boton(10)
crear_etiqueta(10)
crear_entry(10)

####### FRAME 11 ######
crear_etiqueta(11)
cuadroTexto.append(tk.Entry(frames[11]))
cuadroTexto[11].place(x=125,y=105)

botonEnviar=tk.Button(frames[11], text="Enviar", command=codigoBoton,font=("Comic Sans",10),fg="black",activebackground="#90CAF9")
botonEnviar.place(x=200,y=130)
    
botonAtras=tk.Button(frames[11], text="Atras", command=retroceder_pagina,font=("Comic Sans",10),fg="black",activebackground="red")
botonAtras.place(x=125,y=130)






# MAIN LOOP (FINAL)

root.mainloop() #Este metodo 'dibuja' la ventana constantemente. Debera estar al final

