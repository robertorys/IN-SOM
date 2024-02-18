import tkinter as tk
from som import som
from som import dataManager as dm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import matplotlib.pyplot as plt

class interface:
    def __init__(self):
        # Main frame configuration
        self.root = tk.Tk()
        self.root.attributes('-topmost', 1)
        self.root.grid_rowconfigure(0, uniform="rows_g1",weight=1)
        self.root.grid_rowconfigure(1, uniform="rows_g1",weight=1)
        self.root.grid_columnconfigure(0,  uniform="cols_g1",weight=1)
        self.root.grid_columnconfigure(1,  uniform="cols_g1",weight=1)
        self.root.grid_columnconfigure(2,uniform='cols_g1',weight=1)
        self.root.grid_rowconfigure(2, uniform="rows_g1",weight=1)
        
        self.recent_figure = None

        # Frame1: 
        # Creation of the Frame dedicated to graphing the result of the SOM.
        self.som_tk = fm1 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm1.grid(row=0, column=0, rowspan=2,columnspan=2, sticky='nsew')
        self.canvas_som=None
        
        # Frame2: One word
        fm2 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm2.grid(row=0, column=2, sticky='nsew')

        # Label
        tk.Label(fm2, text='Key', bg='white').pack()
        # Entry for a word
        self.one_word_entry=tk.Entry(fm2)
        self.one_word_entry.pack()
        tk.Button(fm2, text='Search key',command=self.search_word).pack()
        # Coordinate label
        self.txtw1 = tk.StringVar()
        tk.Label(fm2, textvariable=self.txtw1, bg='white').pack()
        # BMU label
        self.bmu_w = tk.StringVar()
        tk.Label(fm2, textvariable=self.bmu_w, bg='white').pack()
        # Vector label for word
        self.v_w = tk.StringVar()
        tk.Label(fm2, textvariable=self.v_w, bg='white').pack()
        # Label for the distance between BMU and the word vector.
        self.w_dist = tk.StringVar()
        tk.Label(fm2, textvariable=self.w_dist, bg='white').pack()
        
        # Frame3: Two word
        fm3 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm3.grid(row=1, column=2, sticky='nsew')

        # Label
        tk.Label(fm3, text='Two keys', bg='white').pack()
        #Two Word First Word Entry
        self.tw_1w_e=tk.Entry(fm3)
        self.tw_1w_e.pack()
        self.tw_2w_e=tk.Entry(fm3)
        self.tw_2w_e.pack()
        
        # Button for two words
        tk.Button(fm3, text='Search',command=self.twoword_search).pack()
        
        # Word coordinate label
        self.txtw1vs1_1 = tk.StringVar()
        self.txtw1vs1_2 = tk.StringVar()
        tk.Label(fm3, textvariable=self.txtw1vs1_1, bg='white').pack()
        tk.Label(fm3, textvariable=self.txtw1vs1_2, bg='white').pack()
        
        # BMU1 label
        self.bmu1vs1_w1 = tk.StringVar()
        tk.Label(fm3, textvariable=self.bmu1vs1_w1, bg='white').pack()
        # BMU2 label
        self.bmu1vs1_w2 = tk.StringVar()
        tk.Label(fm3, textvariable=self.bmu1vs1_w2, bg='white').pack()
        
        # Vector label for word 1
        self.v1vs1_w1 = tk.StringVar()
        tk.Label(fm3, textvariable=self.v1vs1_w1, bg='white').pack()
        # Vector label for word 2
        self.u1vs1_w2 = tk.StringVar()  
        tk.Label(fm3, textvariable=self.u1vs1_w2, bg='white').pack()
        
        # Label for the distance between two BMU
        self.bmu1vs1 = tk.StringVar()
        tk.Label(fm3, textvariable=self.bmu1vs1, bg='white').pack()
        
        # Label for the distance between two words
        self.w1vs1 = tk.StringVar()
        tk.Label(fm3, textvariable=self.w1vs1, bg='white').pack()
        
        # Label for the distance between bmu1 and w1
        self.bmu_w1 = tk.StringVar()
        tk.Label(fm3, textvariable=self.bmu_w1, bg='white').pack()
        
        # Label for the distance between bmu2 and w2
        self.bmu_w2 = tk.StringVar()
        tk.Label(fm3, textvariable=self.bmu_w2, bg='white').pack()

        # Frame4: Add file and train SO.
        fm4 = tk.Frame(self.root, bg='white',highlightbackground="black", highlightthickness=2)
        fm4.grid(row=2, column=0, sticky='nsew')
        fm5=tk.Frame(self.root,bg='white',highlightbackground="black", highlightthickness=2)
        fm5.grid(row=2,column=1,sticky='nsew')
        fm6=tk.Frame(self.root,bg='white',highlightbackground="black", highlightthickness=2)
        fm6.grid(row=2,column=2,sticky='nsew')
        
        # Buttons
        tk.Button(fm6,text='Save SOM',command=self.save_som).pack()
        tk.Button(fm4,text="Load SOM",command=self.load_som).pack()
        tk.Button(fm4,text="New SOM",command=self.new_som).pack()
        tk.Button(fm4,text="Load DB",command=self.load_database).pack()
        tk.Button(fm5,text="Train SOM", command=self.som_training).pack()
        tk.Button(fm6,text='Exit',command=self.quit).pack()
        tk.Button(fm5,text="Vecinity", command=self.agrupamiento).pack()
        
        self.progress_text_key=tk.StringVar()
        tk.Label(fm5,textvariable=self.progress_text_key,bg='white').pack()
        self.progress_text_vec=tk.StringVar()
        tk.Label(fm5,textvariable=self.progress_text_vec,bg='white').pack()
        
        self.root.mainloop()
    
    def agrupamiento(self) -> None:
        """ 
        Creates a file with the neighborhood of each key.
        """
        if not self.som.keys_list:
            messagebox.showerror("Needs DB")
            return
        max_vecinity=simpledialog.askinteger("Max Vecinity","max_vecinity=")
        if not max_vecinity or max_vecinity<1:
            messagebox.showerror("Needs valid value")
            return
        
        # Read file with word list
        resultado=''
        index=0
        lista_llaves=self.som.keys_list
        for palabra in lista_llaves:
            self.progress_text_key.set("Progress "+str(index+1)+"/"+str(len(lista_llaves))+" keys")
            resultado+=f"---#{index} {palabra}: {self.som.train_dict[palabra]}---\n"
            bmu_index=self.som.best_matching_unit(self.som.train_dict[palabra])
            vector=self.som.weights[bmu_index]
            resultado+=f"BMU {self.som.coor_from_index(bmu_index)}: {vector}\n"
            resultado+=f"Distance: {som.dist_euclid(self.som.train_dict[palabra], vector)}\n"
            for i in range(1,max_vecinity+1):
                self.progress_text_vec.set("Progress "+str(i)+"/"+str(max_vecinity)+" neighborhood")
                self.root.update()
                resultado+=f"Vecinity {i}:{self.som.vecindario(palabra,i)}\n"
            resultado+='\n'
            index+=1
        self.progress_text_key.set("")
        self.progress_text_vec.set("")
        self.root.update()
        save_path=filedialog.asksaveasfile(filetypes=[("txt files","*.txt")])
        if save_path:
            f=open(save_path.name,'w')
            f.write(resultado)
            f.close()

    def som_training(self)->None:
        """ 
        Initialize training of SOM instance.
        """
        cicles = simpledialog.askinteger("Cicles of training","cicles=")
        if not self.som.keys_list:
            messagebox.showerror("Needs DB")
            return
        if not cicles:
            messagebox.showerror("Needs cicles quantity")
            return
        self.som.init_training(cicles)
        self.update_som_image(self.som.graph())

    def new_som(self) -> None:
        """ 
        Sets a new Instance of SOM to the interface.
        """
        n=simpledialog.askinteger("SOM dimension nxn","n=")
        if not n:
            messagebox.showerror("Needs valid value")
            return

        learn_rate=simpledialog.askfloat("Learning rate","leaning_rate=")
        if learn_rate:
            self.som = som.somObject(n,learning_rate=learn_rate)

    def load_som(self) -> None:
        """
        Loads SOM instance from json.
        """
        json_path=filedialog.askopenfile(filetypes=[("JSON FILES","*.json")])
        if json_path:
            self.som=som.somObject(0,json_path.name)
            self.update_som_image(self.som.graph())
        else:
            messagebox.showerror("Needs SOM json file!")
            return

    def load_database(self) -> None:
        """ Load database using file dialog
        """
        train_data_path=filedialog.askopenfile(filetypes=[("CSV FILES","*.csv")])
        if not train_data_path:
            messagebox.showerror("Needs File path")
            return
        self.som.set_training_data(train_data_path.name)
            
    def save_som(self)->None:
        """ Save SOM on filedialog request
        """    
        file_path=filedialog.asksaveasfile(defaultextension='.json')
        if file_path:
            self.som.save(file_path)
            messagebox.showinfo("File saved succesfully")
        else:
            messagebox.showerror("Error","Needs file path")
        
    def twoword_search(self)->None:
        """
        Searches 2 keys input from the interface. If both are in the list updates canvas.
        """
        k1=self.tw_1w_e.get()
        k2=self.tw_2w_e.get()
        
        if k1 in self.som.keys_list and k2 in self.som.keys_list:
            v = self.som.train_dict[k1]
            u = self.som.train_dict[k2]
            
            fig, i_1, j_1, i_2, j_2, bmu_v, bmu_u = self.som.graphDif(u,v)
            
            self.txtw1vs1_1.set("Coordinates for bmu of w1: ("+str(i_1)+","+str(j_1)+")")
            self.txtw1vs1_2.set("Coordinates for bmu of w2: ("+str(i_2)+","+str(j_2)+")")
            
            self.v1vs1_w1.set("Vector w1: "+str(self.vector_round(v, 2)))
            self.u1vs1_w2.set("Vector w2: "+str(self.vector_round(u, 2)))
            
            self.w1vs1.set("Distance from keys:" + str(round(som.dist_euclid(u,v), 2)))
            
            self.bmu1vs1_w1.set("Bmu w1: "+str(self.vector_round(bmu_v, 2)))
            self.bmu1vs1_w2.set("Bmu w2: "+str(self.vector_round(bmu_u, 2)))
            
            self.bmu1vs1.set("Distance bmu:" + str(round(som.dist_manhattan(bmu_v,bmu_u), 2)))
            
            self.bmu_w1.set("Distance w1 - bmu w1:"+str(round(som.dist_euclid(bmu_v,v), 2)))
            self.bmu_w2.set("Distance w2 - bmu w2:"+str(round(som.dist_euclid(bmu_u,u), 2)))
            
            self.update_som_image(fig)
    
    def reassign_figure(self, new_figure)->None:
        """
        Cleans last figure used in canvas to use new one.

        Args:
            new_figure(matplotlib.figure): New figure to update.
        """
        if self.recent_figure:
            self.recent_figure.clf()
            plt.close(self.recent_figure)
        self.recent_figure=new_figure

    def update_som_image(self,new_figure)->None:
        """
        Updates canvas with new plot.

        Args:
            new_figure(matplotlib.figure): New figure to plot.
        """
        if self.canvas_som:
            self.canvas_som.get_tk_widget().pack_forget()
            self.canvas_som.get_tk_widget().destroy()
        self.reassign_figure(new_figure)
        self.canvas_som=FigureCanvasTkAgg(self.recent_figure,master=self.som_tk)
        self.canvas_som.get_tk_widget().pack()
        
    def search_word(self):
        """
        If the word is in the list. Searches for the word in the matrix and updates the canvas.
        """
        #print(self.one_word_entry.get())
        #print(self.som.training_data.keys())
        
        key = self.one_word_entry.get()
        if key in self.som.keys_list:
            #print(self.som.training_data[self.one_word_entry.get()])
            v = self.som.train_dict[key]
            fig, i, j, bmu = self.som.graphPoint(v)

            self.txtw1.set("Coordenadas: ("+str(i)+","+str(j)+")")
            self.bmu_w.set("Bmu : \n"+str(self.vector_round(bmu, 2)))
            self.v_w.set("Vector : \n"+str(self.vector_round(v, 2)))
            self.w_dist.set("Distancia: \n" + str(round(som.dist_euclid(bmu,v), 2)))
            
            self.update_som_image(fig)

    def quit(self)->None:
        """
        Closes interface.
        """
        self.root.quit()
        self.root.destroy()
    
    def vector_round(self, v: list, n: int) -> list:
        """ Rounds vector values.

        Args:
            v(list): Vector.
            n(int): Decimals to round.
        
        Returns:
            Vector with round values.
        """
        u = []
        for i in v:
            u.append(round(i, n))
        return u
        
a = interface()