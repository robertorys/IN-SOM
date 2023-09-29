import tkinter as tk

class interface:

    def __init__(self):
        # Configuración del frame principal 
        self.root = tk.Tk()
        self.root.wm_attributes('-zoomed', 1)
        self.root.grid_rowconfigure(0, weight=2, uniform="rows_g1")
        self.root.grid_rowconfigure(1, weight=2, uniform="rows_g1")
        self.root.grid_columnconfigure(0, weight=3,  uniform="cols_g1")
        self.root.grid_columnconfigure(1, weight=1,  uniform="cols_g1")

        self.root.grid_rowconfigure(2, weight=1, uniform="rows_g1")
        
        # Frame1: Es para el som
        fm1 = tk.Frame(self.root, bg='red')
        fm1.grid(row=0, column=0, rowspan=2, sticky='nsew')

        # Frame2: Una palabra
        fm2 = tk.Frame(self.root, bg='blue')
        fm2.grid(row=0, column=1, sticky='nsew')

        # Entique
        tk.Label(fm2, text='One word', bg='blue').pack()
        # Entrada para una palabra
        tk.Entry(fm2).pack()
        # botón para una palabra
        tk.Button(fm2, text='Search').pack()

        # Frame3: Dos palabra
        fm3 = tk.Frame(self.root, bg='green')
        fm3.grid(row=1, column=1, sticky='nsew')

        # Entique
        tk.Label(fm3, text='Two words', bg='blue').pack()
        # Entrada para una palabra
        tk.Entry(fm3).pack()
        # Entrada para una palabra
        tk.Entry(fm3).pack()
        # botón para una palabra
        tk.Button(fm3, text='Search').pack()

        # Frame4: Meter archivo y entrenar el som.
        fm4 = tk.Frame(self.root, bg='pink')
        fm4.grid(row=2, column=0, columnspan=2, sticky='nsew')

        # Entique
        tk.Label(fm4, text='Algo va aqui', bg='blue').pack()
        # Entrada para una palabra
        #tk.filedialog(fm4, mode='r').pack()
        # botón para una palabra
        tk.Button(fm4, text='Submit').pack()

        self.root.mainloop()

        
        
        
a = interface()