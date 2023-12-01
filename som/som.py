# Datos de un objeto som:
# - Nombre del som.
# - Tamaño de la matriz.
# - Iteraciones para el entrenamiento.
# - Tasa de aprendizaje.
# - Longitud del vector de peso.
# - Matriz de pesos.

from som import dataManager as dm
import matplotlib.pyplot as plt
import sys
import random
import math


class somObject:
    normsMatrix = []

    # Iniciar el nuevo SOM.
    def __init__(self, n:int, somJson: str = None, learning_rate=0.5):
        if not somJson:
            self.n = n # Tamaño de matriz para los pesos.
            self.training_i = 0 # Cantidad de iteraciones actuales del entrenamiento.
            self.learning_rate = learning_rate # Taza de aprendizaje.
            self.weights = [] # Lista de pesos.
            self.new = True
        else:
            self.jsonData = dm.getJson(somJson) # Json de los datos de un SOM.
            self.n =  self.jsonData['n'] # Tamaño de matriz para los pesos.
            self.training_i = self.jsonData['training_iterations'] # Cantidad de iteraciones actuales del entrenamiento.
            self.weightsLen = self.jsonData['weights_length'] # Tamaño de los vestores de entrenamiento.
            self.learning_rate = learning_rate # Taza de aprendizaje.
            self.weights = self.jsonData['weights'] # Lista de pesos.
            self.new = False
            self.createMatrixM() # Matriz (lista de listas) de nomrmas de los pesos.
        self.train_dict = None
        self.keys_list = None
        self.weightsLen = 0
            
    def set_training_data(self, training_data:str) -> None:
        """ Estable los datos para entrenamiento y calculo de vacinos.

        Args:
            training_data (str): Dirección de un csv con los datos de entranamiento.
        """
        self.train_dict = dm.csv_read_dict(training_data) # Diccionario para los datos de entrenamiento ('key':'vector').
        self.keys_list = list(self.train_dict.keys()) #  Lista de las llaves del diccionario 'train_dict'.
        key = self.keys_list[0] 
        self.weightsLen = len(self.train_dict[key]) # Tamaño de los vestores de entrenamiento.
            
    
    def get_sample(self) -> list:
        """ Regresa un muestreo de los datos de entranamiento.

        Returns:
            list: Lista de las llaves de los datos de muestreo.
        """
        tdl = len(self.keys_list)
        
        if tdl <= self.n:
            return self.keys_list
        else:
            return random.sample(self.keys_list, self.n)
    
    def get_max_min(self) -> tuple:
        """ Regresa el valor maximo y minimo de una muestra de los datos de entrenamiento.

        Returns:
            tuple: regresa una tupla de done el primer elemento es el minimo y el segundo es el máximo.
        """
        sample = self.get_sample()
        max = 0
        min = 1000  
        max_i = self.weightsLen - 1
        for k in sample:
            vector = self.train_dict[k]
            vector.sort()
            if max < vector[max_i]:
                max = vector[max_i]
                
            if min > vector[0]:
                min = vector[0]
        return min, max
                
    def init_weights(self):
        """ 
        Inicializa la matriz de pesos con una distribución unifroma con valores maximos y minimos de una muestra.
        """
        min, max = self.get_max_min()
        for i in range(self.n**2):
            w = []
            for j in range(self.weightsLen):
                w.append(round(random.uniform(min, max), 5))
            self.weights.append(w)
        self.createMatrixM()
        
    def best_matching_unit(self, x:list) -> int:
        """ Regresa el índice de la mejor celula de la matriz de pesos.

        Args:
            x (list): Vector para buscar la celula que más se parace.

        Returns:
            int: Índice de la célula más parecida.
        """
        min = sys.maxsize
        index = 0
        for w in self.weights:
            d = dist_euclid(x, w)
            if d < min:
                min = d
                bmu_i = index
            index += 1
                
        return bmu_i
        
    def update_weight(self, bmu:list, w:list, lr_t:float) -> list:
        """ Actualiza los pesos de una celula con un vector w.

        Args:
            bmu (list): Best Matching Unit (bmu) para 'w'.
            w (list): Vector de un elemento de datos de entrenamiento. 
            lr_t (float): tasa de aprendizaje.

        Returns:
            list: Nuevo vector para la celula.
        """
        for i in range(len(w)):
            w[i] = w[i] + lr_t * (bmu[i] - w[i])  
        return w
            
    def init_training(self):
        """
            Inicia el entrenamiento para el SOM.
        """
        
        if self.new:
            self.init_weights()
        
        count = 1
        lambda_ = self.cicles / 2
        nr_t0 = self.n / 4
        
        # Entrenamiento      
        for i in range(self.cicles):
            t = i + 1 
            
            # Calculate neighbourhiood radius
            nr_t = nr_t0 * math.exp(-t/lambda_)
            
            # Calculete learning rate 
            lr_t = self.learning_rate * math.exp(-t/lambda_)
            
            key = random.sample(self.keys_list, 1) # Obtener la llave para un dato de entrenamiento.
            unique_sample = self.train_dict[key[0]]# Al obtener key es una lista de un solo elemento
            bmu = self.best_matching_unit(unique_sample) # Indice del la celula más parecida al dato para entrenamiento.

            # Actualización de los vecinos.
            # i / n = fila
            # i % n = columna
            
            bmu_i , bmu_j = self.coor_from_index(bmu)
            
            wi = 0
            for w in self.weights:
                wi_i , wi_j = self.coor_from_index(wi)
                
                if dist_manhattan([bmu_i, bmu_j], [wi_i, wi_j]) < nr_t:
                    self.weights[wi] = self.update_weight(unique_sample, w, lr_t)
                wi += 1
            self.training_i += 1
            
            if count == 100:
                print('cicles:', self.training_i)
                count = 0
            count += 1
        
        self.createMatrixM()
        
    

    def vecindario(self, key, vecinity:int) -> list:
        """ De una palabra (llave) cuales palabras (llaves) de la lista pertenecen a su vecindario de distancia 'vecinity'.

        Args:
            key (_type_): Llave para un dato de entrenamiento.
            vecinity (int): Distancia del vecindario.
            list_keys (list): Lista de llaves para comparar si pertenece al vecindario.

        Returns:
            list: Lista de llaves que si pertenencen al veciendario.
        """
        bmu_key=self.best_matching_unit(self.train_dict[key])
        bmu_keys = [self.best_matching_unit(self.train_dict[k]) for k in self.keys_list] # Lista de indices del 'bmu' de cada llave.
        matriz = [] # Lista que contiene todas los indices del vecindario para 'key'.
        
        for i in range(- vecinity, vecinity + 1):
            for j in range(- vecinity, vecinity + 1):
                matriz.append((i * self.n + j) + bmu_key)
                
        vecinos_indice = [indice for indice in range(len(bmu_keys)) if bmu_keys[indice] in matriz and bmu_keys[indice] != bmu_key]
        vecinos=[self.keys_list[indice] for indice in vecinos_indice ]
        return vecinos
    
    def createMatrixM(self) -> None:
        """
         Creación de una maatriz de normas de los vectores de pesos.
        """
        self.normsMatrix=[]
        index = 0
        for i in range(self.n):
            ni = []
            for j in range(self.n):
                ni.append(norm(self.weights[index]))
                index += 1
            self.normsMatrix.append(ni)
            
    def graph(self) -> plt.figure:
        """ Grafica la matriz de pesos del SOM.

        Returns:
            plt.figure: Una figura de matplotlib.pyplot.figure
        """
        fig=plt.figure()
        plt.pcolor(self.normsMatrix, cmap='jet_r')  # Mapa de calor de la distancia de las unidades
        plt.colorbar()
        return fig
        
    def graphPoint(self, x:list) -> plt.figure:
        """ Grafica la matriz de pesos del SOM y la ubicación del bmu para un vector.

        Args:
            x (list): Vector para buscar su 'bmu'.

        Returns:
            plt.figure: Una figura de matplotlib.pyplot.figure
        """
        fig=plt.figure()
        bmu = self.best_matching_unit(x) # Indice del la celula más parecida al dato para entrenamiento.
    
        bmu_i,bmu_j = self.coor_from_index(bmu)
        
        # Consultar vector del bmu.
        bmu_v = self.weights[bmu]
        
        plt.pcolor(self.normsMatrix, cmap='jet_r')  # Mapa de calor de la distancia de las unidades
        plt.plot(bmu_i,bmu_j,marker ="x",color='black')
        
        return fig, bmu_i, bmu_j, bmu_v
    
    def graphDif(self, v:list, u:list) -> plt.figure:
        """ Grafica la matriz de pesos del SOM y una recta entre dos vector de su 'bmu'.

        Args:
            v (list): Vector v para una palabra.
            u (list): Vector u para una palabra.

        Returns:
            plt.figure: Una figura de matplotlib.pyplot.figure
        """
        fig=plt.figure()
        bmu_v = self.best_matching_unit(v) # Índice del la celula más parecida del vector v.
        bmu_u = self.best_matching_unit(u) # Índice del la celula más parecida del vector u.
        
        v_i,v_j = self.coor_from_index(bmu_v)
        
        u_i,u_j = self.coor_from_index(bmu_u)
        
        plt.pcolor(self.normsMatrix, cmap='jet_r')  # Mapa de calor de la distancia de las unidades
        plt.plot([u_i, v_i],[u_j, v_j],color='black')
        return fig, v_i, v_j, u_i, u_j, self.weights[bmu_v], self.weights[bmu_u]
    
    def coor_from_index(self, index:int)->tuple:
        """ Coordenadas de tipo matriz para una lista de listas.

        Args:
            index (int): índice de una lista.

        Returns:
            tuple: Regresa los dos índices (i,j).
        """
        bmu_i = math.floor(index / self.n) # fila del bmu.
        bmu_j = index % self.n # columna del bmu.
        return (bmu_i,bmu_j)
    
    # ---------- Formato Json ---------- #
    
    # Guardar datos en formato json
    def save(self, nameSom:str, nameFile:str) -> None:
        
        self.jsonData['name'] = nameSom
        self.jsonData['n'] = self.n
        self.jsonData['training_iterations'] = self.training_i
        self.jsonData['training_rate'] = self.learning_rate
        self.jsonData['weights_length'] = self.weightsLen
        self.jsonData['weights'] = self.weights
        
        
        dm.saveJson(self.jsonData, nameFile)

    def GetDict(self) -> dict:
        return dm.csv_read_dict(self.strt)
                
# ----------Operaciones con vectores ----------#

# Norma para un vector.
def norm(x:list) -> float:
    sum = 0
    for i in range(len(x)):
        sum += x[i]**2
        
    return math.sqrt(sum)

# Distancia eucidiana para dos vectores.   
def dist_euclid(x:list, y:list) -> float:
    sum = 0
    if len(x)!=len(y):
        print(f"Error x:{len(x)}, y:{len(y)}")
    for i in range(len(x)):
        sum +=  (x[i] - y[i])**2
    return math.sqrt(sum)

# Distancia de manhattan para dos vectores. 
def dist_manhattan(x:list, y:list) -> int:
    sum = 0
    for i in range(len(x)):
        sum += abs(x[i] - y[i])
    return sum       

# Cosine similarity bweteen two vectors.
def cos_simi(x:list, y:list) -> float:
    pp = 0
    mod_x = 0
    mod_y = 0
    
    for i in range(len(x)):
        pp += (x[i] * y[i])
        mod_x += x[i]**2
        mod_y += y[i]**2
        
    mod_x = math.sqrt(mod_x)
    mod_y = math.sqrt(mod_y)
    
    return pp/(mod_x * mod_y)
