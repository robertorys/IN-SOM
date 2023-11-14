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
        self.root.attributes('-zoomed', 1)
        self.root.grid_rowconfigure(0, uniform="rows_g1")
        self.root.grid_rowconfigure(1, uniform="rows_g1")
        self.root.grid_columnconfigure(0,  uniform="cols_g1")
        self.root.grid_columnconfigure(1,  uniform="cols_g1")
        self.root.grid_columnconfigure(2,uniform='cols_g1')
        self.root.grid_rowconfigure(2, uniform="rows_g1")
        #Objeto SOM para obtener el SOM, entrenar etc.
        # self.som = som.somObject(100, 1000, '/home/dev212/Robotica_Corporizada/IN-SOM/som/data/sensorimotor.csv', '/home/dev212/Robotica_Corporizada/IN-SOM/som/som_test_1_100x100.json')
        
        self.recent_figure=None
        # Frame1: Es para el som
        #Creacion del Frame dedicado a graficar el resultado del SOM
        self.som_tk=fm1 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm1.grid(row=0, column=0, rowspan=2,columnspan=2, sticky='nsew')
        #Canvas que maneja la figura de matplot para graficar sobre el tkinter
        self.canvas_som=None
        #self.update_som_image(self.som.graph())
        
        # Frame2: Una palabra
        #Creacion del frame contenedor
        fm2 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm2.grid(row=0, column=2, sticky='nsew')
    
        # Etiqueta
        tk.Label(fm2, text='Una palabra', bg='white').pack()
        # Entrada para una palabra
        #Leer entrada al pulsar boton
        self.one_word_entry=tk.Entry(fm2)
        self.one_word_entry.pack()
        # Botón para una palabra
        tk.Button(fm2, text='Buscar una palabra',command=self.search_word).pack()
        # Etiqueta de las coordenadas
        self.txtw1 = tk.StringVar()
        tk.Label(fm2, textvariable=self.txtw1, bg='white').pack()

        # Frame3: Dos palabra
        fm3 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm3.grid(row=1, column=2, sticky='nsew')

        # Entique
        tk.Label(fm3, text='Two words', bg='white').pack()
        # Entrada para una palabra
        #Two Word First Word Entry
        self.tw_1w_e=tk.Entry(fm3)
        self.tw_1w_e.pack()
        self.tw_2w_e=tk.Entry(fm3)
        self.tw_2w_e.pack()
        
        # Botón para dos palabra
        tk.Button(fm3, text='Search',command=self.twoword_search).pack()
        
        # Etiqueta de coordenadas de las palabras
        self.txtw1vs1_1 = tk.StringVar()
        self.txtw1vs1_2 = tk.StringVar()
        tk.Label(fm3, textvariable=self.txtw1vs1_1, bg='white').pack()
        tk.Label(fm3, textvariable=self.txtw1vs1_2, bg='white').pack()
        

        # Frame4: Meter archivo y entrenar el som.
        fm4 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm4.grid(row=2, column=0, sticky='nsew')
        fm5=tk.Frame(self.root,bg='white',highlightbackground="black", highlightthickness=2)
        fm5.grid(row=2,column=1,sticky='nsew')
        fm6=tk.Frame(self.root,bg='white',highlightbackground="black", highlightthickness=2)
        fm6.grid(row=2,column=2,sticky='nsew')
        # Entique
        #tk.Label(fm4, text='Guardar SOM', bg='white').pack()
        # Entrada para una palabra
        #tk.filedialog(fm4, mode='r').pack()
        # botón para una palabra
        tk.Button(fm6,text='Guardar SOM',command=self.save_som).pack()
        tk.Button(fm4,text="Cargar SOM",command=self.load_som).pack()
        tk.Button(fm4,text="Nuevo SOM",command=self.new_som).pack()
        tk.Button(fm5,text="Entrenar SOM", command=self.som_training).pack()
        tk.Button(fm6,text='Exit',command=self.quit).pack()
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
        self.som.init_weights()
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
        file_path=filedialog.asksaveasfile(defaultextension='.json')
        if file_path:
            messagebox.showinfo("Archivo guardado con exito")
        else:
            messagebox.showerror("Error","Se requiere una dirección para guardar")
        
    def twoword_search(self)->None:
        """
        Si tenemos las 2 palabras en el diccionario entonces usamos graphDIF
        """
        k1=self.tw_1w_e.get()
        k2=self.tw_2w_e.get()
        
        if k1 in self.som.keys_list and k2 in self.som.keys_list:
            v = self.som.train_dict[k1]
            u = self.som.train_dict[k2]
            fig, i_1, j_1, i_2, j_2 = self.som.graphDif(u,v)
            self.txtw1vs1_1.set("("+str(i_1)+","+str(j_1)+")")
            self.txtw1vs1_2.set("("+str(i_2)+","+str(j_2)+")")
            self.update_som_image(fig)

    
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
        
        key = self.one_word_entry.get()
        if key in self.som.keys_list:
            #print(self.som.training_data[self.one_word_entry.get()])
            v = self.som.train_dict[key]
            fig, i, j = self.som.graphPoint(v)
            self.txtw1.set("("+str(i)+","+str(j)+")")
            self.update_som_image(fig)

        
            
    def quit(self)->None:
        self.root.destroy()
        
a = interface()