import tkinter as tk
from tkinter import *

# CPH = cosas por hacer.
# DEF = definición.

class interface:
    root = tk.Tk()
    frame = tk.Frame(root)

    # DEF: Input box para ubicar una palabra.
    oneWordEntry = tk.Entry()

    # DEF: 2 inputs box para la dis
    fTwoWordsEntry = tk.Entry()
    sTwoWordsEntry = tk.Entry()

    # CPH: Crear un chek box, para indicar si la palabra unica va a regresar un "sub som".

    # CPH: Dos botones para hacer que funcione la lógica de las palabras.

    # CPH: Div para el gráfico.

    # CPH: Una entrada y boton para subir archivo de entenamiento.
    # CPH: Un botón para hacer el entrenamiento.

    
    def __init__(self):
        self.root.mainloop()


    # CPH: Muestra el grafico del som.
    def intSom(self):

    # CPH: Lógica para una sola palabra.
    def oneWord(self):

    # CPH: Lógica para mostrar el sub som.
    def subSOM(self):

    # CPH: Lógica para la distabcia de dos palabras
    def disTwoWords(self):

    # CPH: Cargar un arhivo.
    def submit(self):

    # CPH: Cargar el entrenamiento del SOM.
    def entSOM(self):


vi = interface()
