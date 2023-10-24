import tkinter as tk
from som import somObject

class interface:

    def __init__(self):
        # Configuración del frame principal 
        self.root = tk.Tk()
        self.root.wm_attributes('-zoomed', 1)
        self.root.grid_rowconfigure(0, weight=3, uniform="rows_g1")
        self.root.grid_rowconfigure(1, weight=3, uniform="rows_g1")
        self.root.grid_columnconfigure(0, weight=3,  uniform="cols_g1")
        self.root.grid_columnconfigure(1, weight=1,  uniform="cols_g1")

        self.root.grid_rowconfigure(2, weight=1, uniform="rows_g1")
        
        # Frame1: Es para el som
        fm1 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm1.grid(row=0, column=0, rowspan=2, sticky='nsew')
        
        som = somObject(100, 1000, '/data/sensorimotor.csv', 'som_test_1_100x100.json')
        a = [2.214,0,0.429,0,0,2.429,0,0.357,1.071,0.357,0]
        img = som.graphPoint(a)
        
        label = tk.Label(fm1, img)
        label.pack()
        # Funcion para graficar SOM
        
        # Frame2: Una palabra
        fm2 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm2.grid(row=0, column=1, sticky='nsew')

        # Etiqueta
        tk.Label(fm2, text='One word', bg='white').pack()
        # Entrada para una palabra
        tk.Entry(fm2).pack()
        # botón para una palabra
        tk.Button(fm2, text='Search').pack()

        # Frame3: Dos palabra
        fm3 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm3.grid(row=1, column=1, sticky='nsew')

        # Entique
        tk.Label(fm3, text='Two words', bg='white').pack()
        # Entrada para una palabra
        tk.Entry(fm3).pack()
        # Entrada para una palabra
        tk.Entry(fm3).pack()
        # botón para una palabra
        tk.Button(fm3, text='Search').pack()

        # Frame4: Meter archivo y entrenar el som.
        fm4 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm4.grid(row=2, column=0, columnspan=2, sticky='nsew')

        # Entique
        tk.Label(fm4, text='Algo va aqui', bg='white').pack()
        # Entrada para una palabra
        #tk.filedialog(fm4, mode='r').pack()
        # botón para una palabra
        tk.Button(fm4, text='Submit').pack()

        self.root.mainloop()
        
a = interface()