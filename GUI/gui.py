# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import ttk

########## CREACION VENTANA RAIZ #############

root=tk.Tk() #creamos una varibale de instancia de la clase tk. Crea la ventana principal e inicia interpetre Tcl/Tk
root.title("VoIP Network Designer") #titulo ventana
root.config(width=600, height=400) #dimensiones ventana

########## FRAME 1 ##########
frame1=tk.Frame(root) # FRAME 1 sera hijo de root (herencia)
frame1.pack(fill="both", expand=1) #empaquetamos este frame (es decir se hace visible) del tamaño de root
frame1.config(width=600, height=400)

etiqueta_mos=ttk.Label(frame1, text="Introduzca el MOS minimo") #creamos instancia ttk etiqueta: mensaje que se muestra en la ventana
etiqueta_mos.place(x=20,y=20) #debemos indicar la posicion del mensaje
#etiqueta_mos.pack()

caja_mos=ttk.Entry(frame1)
caja_mos.place(x=160, y=20, width=60)
#caja_mos.pack()

boton_mos=ttk.Button(frame1, text='Siguiente') #command=enviar_dato
boton_mos.place(x=20, y=60)
#boton_mos.pack()

############ FRAME 2 #############







# MAIN LOOP (FINAL)

root.mainloop() #Este metodo 'dibuja' la ventana constantemente. Debera estar al final