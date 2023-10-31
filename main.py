import tkinter as tk
from som import som
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import matplotlib.pyplot as plt

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
        #Objeto SOM para obtener el SOM, entrenar etc.
        self.som = som.somObject(100, 1000, '/home/dev212/Robotica_Corporizada/IN-SOM/som/data/sensorimotor.csv', '/home/dev212/Robotica_Corporizada/IN-SOM/som/som_test_1_100x100.json')
        self.recent_figure=None
        # Frame1: Es para el som
        #Creacion del Frame dedicado a graficar el resultado del SOM
        self.som_tk=fm1 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm1.grid(row=0, column=0, rowspan=2, sticky='nsew')
        #Canvas que maneja la figura de matplot para graficar sobre el tkinter
        self.canvas_som=None
        self.update_som_image(self.som.graph())
        
        # Frame2: Una palabra
        #Creacion del frame contenedor
        fm2 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm2.grid(row=0, column=1, sticky='nsew')

        # Etiqueta
        tk.Label(fm2, text='Una palabra', bg='white').pack()
        # Entrada para una palabra
        #Leer entrada al pulsar boton
        self.one_word_entry=tk.Entry(fm2)
        self.one_word_entry.pack()
        # botón para una palabra
        tk.Button(fm2, text='Buscar una palabra',command=self.search_word).pack()

        # Frame3: Dos palabra
        fm3 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm3.grid(row=1, column=1, sticky='nsew')

        # Entique
        tk.Label(fm3, text='Two words', bg='white').pack()
        # Entrada para una palabra
        #Two Word First Word Entry
        self.tw_1w_e=tk.Entry(fm3)
        self.tw_1w_e.pack()
        self.tw_2w_e=tk.Entry(fm3)
        self.tw_2w_e.pack()
        #
        # botón para una palabra
        tk.Button(fm3, text='Search',command=self.twoword_search).pack()
        

        # Frame4: Meter archivo y entrenar el som.
        fm4 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm4.grid(row=2, column=0, columnspan=2, sticky='nsew')

        # Entique
        tk.Label(fm4, text='Guardar SOM', bg='white').pack()
        # Entrada para una palabra
        #tk.filedialog(fm4, mode='r').pack()
        # botón para una palabra
        tk.Button(fm4, text='Guardar SOM',command=self.save_som).pack()
        tk.Button(fm4,text="Cargar SOM",command=self.load_som).pack()
        tk.Button(fm4,text="Nuevo SOM",command=self.new_som).pack()
        tk.Button(fm4,text="Entrenar SOM", command=self.som_training).pack()

        self.root.mainloop()

    def som_training(self)->None:
        self.som.init_training()
        self.update_som_image(self.som.graph())

    def new_som(self)->None:
        n=simpledialog.askinteger("Dimension del SOM","n=")
        if not n:
            messagebox.showerror("Se necesita la dimension del SOM")
            return
        cicles=simpledialog.askinteger("Ciclos","cicles=")
        if not cicles:
            messagebox.showerror("Se necesita la cantidad de ciclos")
            return
        train_data_path=filedialog.askopenfile(filetypes=[("CSV FILES","*.csv")])
        if not train_data_path:
            messagebox.showerror("Necesitamos la información de entrenamiento")
            return
        learn_rate=simpledialog.askfloat("Razon de aprendizaje","leaning_rate=")
        if learn_rate:
            self.som=som.somObject(n,cicles,train_data_path.name,learning_rate=learn_rate)
        else:
            self.som=som.somObject(n,cicles,train_data_path.name)
        self.update_som_image(self.som.graph())

    def load_som(self)->None:
        train_data_path=filedialog.askopenfile(filetypes=[("CSV FILES","*.csv")])
        if not train_data_path:
            messagebox.showerror("Necesitamos la información de entrenamiento")
            return
        json_path=filedialog.askopenfile(filetypes=[("JSON FILES","*.json")])
        if json_path:
            self.som=som.somObject(0,0,train_data_path.name,json_path.name)
            self.update_som_image(self.som.graph())
        else:
            messagebox.showerror("Necesitamos el archivo json que contiene el SOM")
        return

    def save_som(self)->None:
        name=simpledialog.askstring("Nombre del SOM","Ingrese el nombre : ")
        if name:
            file_path=filedialog.asksaveasfile(defaultextension='.json')
            if file_path:
                self.som.save(name,file_path.name)
                messagebox.showinfo("Archivo guardado con exito")
            else:
                messagebox.showerror("Error","Se requiere una dirección para guardar")
        else:
            messagebox.showerror("Error","Se necesita asignar un nombre")

    def twoword_search(self)->None:
        """
        Si tenemos las 2 palabras en el diccionario entonces usamos graphDIF
        """
        w1=self.tw_1w_e.get()
        w2=self.tw_2w_e.get()
        #print(w1)
        #print(w2)
        if w1 in self.som.training_data and w2 in self.som.training_data:
            #print(self.som.training_data[w1])
            #print(self.som.training_data[w2])
            self.update_som_image(self.som.graphDif(self.som.training_data[w1],self.som.training_data[w2]))

    
    def reassign_figure(self, new_figure)->None:
        """
        Limpia la figura utilizada en el canvas y asigna la nueva
        """
        if self.recent_figure:
            self.recent_figure.clf()
            plt.close(self.recent_figure)
        self.recent_figure=new_figure

    def update_som_image(self,new_figure)->None:
        """
        Actualiza el canvas asignandole la nueva figura
        """
        if self.canvas_som:
            self.canvas_som.get_tk_widget().pack_forget()
            self.canvas_som.get_tk_widget().destroy()
        self.reassign_figure(new_figure)
        self.canvas_som=FigureCanvasTkAgg(self.recent_figure,master=self.som_tk)
        self.canvas_som.get_tk_widget().pack()
        

    def search_word(self):
        """
        Si la palabra esta en el diccionario entonces
            Actualiza el canvas al pasarle la figura que regresa el plot, pasandole la lista que vincula la llave
        """
        #print(self.one_word_entry.get())
        #print(self.som.training_data.keys())
        if self.one_word_entry.get() in self.som.training_data:
            #print(self.som.training_data[self.one_word_entry.get()])
            self.update_som_image(self.som.graphPoint(self.som.training_data[self.one_word_entry.get()]))
            

        
a = interface()