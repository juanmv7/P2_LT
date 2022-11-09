# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import ttk

#Crear y avanzar frame sera lo mismo. Esto implica que cada vez que volvamos atras, debemos volver a rellenar (y por tanto reecribir) el frame
def crear_frame:
    if i>0:
        frames[i].forget()
        i++
    frames[i]=tk.Frame(root, width=600, height=400)
    frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame

#Al retroceder no se modifica el frame, pero luego al volver al avanzar si que tendremos que reescribirlo!
def retroceder_pagina:
    frames[i].forget()# dejamos de visualizar este frame
    i-- #iteramos
    frames[i].pack(fill='both', expand=1) #mostramos el siguiente frame

########## CREACION VENTANA RAIZ #############

root=tk.Tk() #creamos una varibale de instancia de la clase tk. Crea la ventana principal e inicia interpetre Tcl/Tk
root.title("VoIP Network Designer") #titulo ventana
root.config(width=600, height=400) #dimensiones ventana
frames=[10] #vector donde guardaremos los distintos frames o paginas del programa
i=0 #para iterar entre frames

########## FRAME 1 ##########
crear_frame()# FRAME 1 sera hijo de root (herencia)
frames[i].pack(fill="both", expand=1) #empaquetamos este frame (es decir se hace visible) y ocupa toda la ventana (si el frame no tiene nada es 0x0 pixel)
frames[i].config()

etiqueta_mos=ttk.Label(frames[i], text="Introduzca el MOS minimo") #creamos instancia ttk etiqueta: mensaje que se muestra en la ventana
etiqueta_mos.pack()
etiqueta_mos.place(x=20,y=20) #debemos indicar la posicion del mensaje

caja_mos=ttk.Entry(frames[i])
caja_mos.pack()
caja_mos.place(x=200, y=20, width=60)

boton_mos=ttk.Button(frames[i], text='Siguiente', command=avanzar_pagina) #command=enviar_dato
boton_mos.pack()
boton_mos.place(x=20, y=60)

############ FRAME 2 #############







# MAIN LOOP (FINAL)

root.mainloop() #Este metodo 'dibuja' la ventana constantemente. Debera estar al final