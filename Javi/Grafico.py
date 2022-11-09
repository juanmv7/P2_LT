from tkinter import *

raiz=Tk() #Crea ventana principal

raiz.title("Práctica 2") #Poner titulo ventana
raiz.resizable(TRUE,TRUE) #Para poder redimensionar tamaño ventana (ancho,alto)
raiz.iconbitmap("LT_Simbolo.ico") #Poner icono
#raiz.geometry("650x350") #Cambiar tamaño
miFrame=Frame(raiz, width=650,height=350)

miFrame.pack()
MOS=0
#miFrame.configure(bg='red')
#miImagen=PhotoImage(file="........") #Añadir foto debemos hacer label con image=miImagen

#-------------------------------Config--------------------------------
valorMOS=StringVar()
miLabel=Label(miFrame, text="Introduzca valores de MOS:", fg="blue")
miLabel.place(x=240,y=10)
cuadroTexto=Entry(raiz,textvariable=valorMOS)
cuadroTexto.place(x=250,y=30)
#-------------------------------Cuadro textos--------------------------------

def codigoBoton():
    
   MOS=float(valorMOS.get())
   print(MOS)
   if MOS==5:
    print("El valor es bueno")
    miLabel2.config(text="Has escogido el codec 2", fg="blue")
    
    

botonEnviar=Button(raiz, text="Enviar",command=codigoBoton)
botonEnviar.place(x=250,y=50)
botonAtras=Button(raiz, text="Atras",command=codigoBoton)
botonAtras.place(x=330,y=50)
miLabel2=Label(raiz)
miLabel2.place(x=240,y=90)
#-------------------------------Boton--------------------------------


raiz.mainloop() #Dibuja la ventana constantemente debe ir al final




