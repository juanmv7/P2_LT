# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import *
from tkinter import messagebox

#from PIL import ImageTk, Image
import socket

#VARIABLES GLOBALES
i=0 #para iterar entre frames
frames=[] #vector donde guardaremos los distintos frames o paginas del programa
valores=[]
cuadroTexto=[]
mensaje=["Introduzca el valor deseado del MOS:", "Introduzca el retardo requerido (ms):", "Introduzca el retardo de red (ms):", "    Introduzca el jitter total (ms):","Introduzca el número de clientes (Nc):" ,"Introduzca el numero de líneas \n por cliente (Nl):", "Introduzca el tiempo medio por \n llamada (Tpll)(Min):" ,"   Introduzca la probabilidad \n de bloqueo (%):","  Introduzca el ancho de banda \n de reserva (%):" ,"  Introduzca el ancho de banda \n requerido (bps):", "Indica si desea compresion cRTP  \n (Yes=1 No=0):","Introduzca el tipo de encapsulación:\n  - Ethernet --> 1\n  - Ethernet 802.1q --> 2\n  - Ethernet q-in-q --> 3\n  - PPPOE: --> 4\n  - PPPOE 802.1q: --> 5"]



#Crear y avanzar frame sera lo mismo. Esto implica que cada vez que volvamos atras, debemos volver a rellenar (y por tanto reecribir) el frame
def crear_frame():
    global frames
    frames.append(tk.Frame(root, width=400, height=200,bg="lightblue"))


#Al retroceder no se modifica el frame, pero luego al volver al avanzar si que tendremos que reescribirlo!
def retroceder_pagina():
    global i, frames, valores
    valores.pop()
    frames[i].forget()# dejamos de visualizar este frame
    i=i-1 #iteramos
    frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame


def crear_boton(k):
    
    botonEnviar=tk.Button(frames[k], text="Enviar", command=codigoBoton,font=("Comic Sans",10),fg="black",bg="lightblue",activebackground="#5ccb5f")
    botonEnviar.place(x=205,y=85)
    if(k>0):
        botonAtras=tk.Button(frames[k], text="Atras", command=retroceder_pagina,font=("Comic Sans",10),fg="black",bg="lightblue",activebackground="red")
        botonAtras.place(x=130,y=85)


def crear_etiqueta(k):
    global mensaje
    miLabel=tk.Label(frames[k], text=mensaje[k], fg="blue",bg="lightblue")
    miLabel.place(x=100,y=10)
    

def crear_entry(k):
    global cuadroTexto
    cuadroTexto.append(tk.Entry(frames[k]))
    cuadroTexto[k].config(justify=CENTER)
    cuadroTexto[k].place(x=130,y=60)


def codigoBoton():
    global i, frames, valores
     
    valores.append(cuadroTexto[i].get())
    check_errors()
    #  if(valores[i]!=''): #Control error con 0 y ""
    conectar_server()
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

def check_errors():
    global valores
    
    if ((valores[i].isspace()) or (valores[i]=='')):
        messagebox.showerror('VoIP Network Designer', 'Error: No ha introducido nada. Vuelva Atrás.')
    
    if ((valores[i].isalpha())):
        messagebox.showerror('VoIP Network Designer', 'Error: La entrada no se esperaba alfanumérica. Vuelva Atrás')
        
        
def conectar_server():
    global i, solucion
    # Programa Cliente
    # Creando un socket TCP/IP
    sock = socket.socket()

    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = ('localhost', 10800)
    print ('conectando a %s puerto %s' % server_address)
    sock.connect(server_address)
    if(i<11 or i==12):

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
        print ('Llega "%s"' % data)
        solucion=data.decode(('utf-8'))
        label_solucion(solucion)
        
        sock.close()


def label_solucion(solucion):
    
    solucion=solucion.split("-")
    if(solucion[3]=="False" or solucion[6]=="False"):
        solucion[3]="NO"
        solucion[6]="NO"
    if(solucion[3]=="True" or solucion[6]=="True"):
        solucion[3]="SI"
        solucion[6]="SI"
    solucion_Final="\n -El MOS elegido es: "+ solucion[0] + "\n -El Codec elegido es: " + solucion[1]+ "\n -El retardo calculado es: "+ solucion[2]+ " ms \n -El retardo requerido " + solucion[3]+ " cumple con las especificaciones del codec elegido" + "\n -El número de líneas es: "+ solucion[4]+ "\n-El ancho de banda resultante es: "+ solucion[5]+" bps \n-El ancho de banda pedido "+solucion[6]+" cumple con las especificaciones del codec elegido"
   
    miLabel=tk.Label(frames[12], text=solucion_Final, fg="blue",bg="lightblue")
    miLabel2=tk.Label(frames[12], text="Informe Resultados:", fg="black",bg="lightblue",font=("Comic Sans",12,"bold"))
    miLabel3=tk.Label(frames[12], text="Introduzca su correo para \n un informe más detallado:", fg="black",bg="lightblue")
    miLabel.place(x=100,y=40)
    miLabel2.place(x=250,y=20) 
    miLabel3.place(x=90,y=190)

def enviar_correo():
    global i

    valores.append(cuadroTexto[i].get())
    conectar_server()
    miLabel4=tk.Label(frames[12], text="Se ha enviado el informe a su correo.", fg="green",bg="lightblue",font=("Comic Sans",10))
    miLabel4.place(x=230,y=260)



########## CREACION VENTANA RAIZ #############

root=tk.Tk() #creamos una varibale de instancia de la clase tk. Crea la ventana principal e inicia interpetre Tcl/Tk
root.title("VoIP Network Designer") #titulo ventana
root.config(width=600, height=300) #dimensiones ventana
root.iconbitmap("LT_Simbolo.ico")
root.resizable(0,0)


for k in range(0,12):
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
cuadroTexto[11].config(justify=CENTER)
cuadroTexto[11].place(x=125,y=105)

botonEnviar=tk.Button(frames[11], text="Enviar", command=codigoBoton,font=("Comic Sans",10),fg="black",activebackground="#5ccb5f")
botonEnviar.place(x=200,y=130)
    
botonAtras=tk.Button(frames[11], text="Atras", command=retroceder_pagina,font=("Comic Sans",10),fg="black",activebackground="red")
botonAtras.place(x=125,y=130)

####### FRAME 12 ######
frames.append(tk.Frame(root, width=600, height=400,bg="lightblue"))

cuadroTexto.append(tk.Entry(frames[12]))
cuadroTexto[12].config(justify=CENTER)
cuadroTexto[12].place(x=250,y=200)


botonEnviar=tk.Button(frames[12], text="Enviar Correo", command=enviar_correo,font=("Comic Sans",10),fg="black",bg="lightblue",activebackground="#5ccb5f")
botonEnviar.place(x=325,y=225)
    
botonAtras=tk.Button(frames[12], text="Atras", command=retroceder_pagina,font=("Comic Sans",10),fg="black",bg="lightblue",activebackground="red")
botonAtras.place(x=245,y=225)

# MAIN LOOP (FINAL)

root.mainloop() #Este metodo 'dibuja' la ventana constantemente. Debera estar al final

