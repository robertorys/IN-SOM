from som import dataManager as dm
import matplotlib.pyplot as plt
import sys
import random
import math


class somObject:
    n: int
    cicles:int
    training_i: int
    weightsLen:int
    learning_rate: float
    weights: list
    new: bool
    jsonData:dict
    train_dict: dict
    keys_list: list
    normsMatrix:list

    # Iniciar el nuevo SOM.
    def __init__(self, n:int, somJson: str = None, learning_rate=0.5):
        """Initialize SOM object with parameters

        Args:
            n(int): Matrix size nxn.
            somJson(str): File Path to json with SOM object.
            learning_rate(float): Learning rate hyperparameter for SOM training.
        Return:
            SOM instance.
        """
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
        """ Sets training data for the training and calculating the neighborhood

        Args:
            training_data (str): File path to the csv with the training data.
        """
        self.train_dict = dm.csv_read_dict(training_data) # Diccionario para los datos de entrenamiento ('key':'vector').
        self.keys_list = list(self.train_dict.keys()) #  Lista de las llaves del diccionario 'train_dict'.
        key = self.keys_list[0] 
        self.weightsLen = len(self.train_dict[key]) # Tamaño de los vestores de entrenamiento.
    
    def get_sample(self) -> list:
        """ Returns a sample of the keys from training.

        Returns:
            list: Sample of keys.
        """
        tdl = len(self.keys_list)
        
        if tdl <= self.n:
            return self.keys_list
        else:
            return random.sample(self.keys_list, self.n)
    
    def get_max_min(self) -> tuple:
        """ Returns max and min values from a sample of the training data.

        Returns:
            tuple: Tuple where the first value is min and the second value is max.
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
                
    def init_weights(self) -> None:
        """ 
        Initializes the matrix of weights with an uniform distribution with max and min values obtaines from a sample.
        """
        min, max = self.get_max_min()
        for i in range(self.n**2):
            w = []
            for j in range(self.weightsLen):
                w.append(round(random.uniform(min, max), 5))
            self.weights.append(w)
        self.createMatrixM()
        
    def best_matching_unit(self, x:list) -> int:
        """ Returns index from the best matching unit in the matrix of weights.

        Args:
            x (list): Vector used for searching the best matching unit.

        Returns:
            int: Index from the BMU.
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
        """ Updates weights on w using bmu.
            
        Args:
            bmu (list): Best Matching Unit (bmu) vector.
            w (list): Vector for update. 
            lr_t (float): Learning rate.

        Returns:
            list: Updated weight.
        """
        for i in range(len(w)):
            w[i] = w[i] + lr_t * (bmu[i] - w[i])  
        return w
            
    def init_training(self, cicles: int) -> None:
        """ Initialize SOM training using the cicles as limit.

        Args:
            cicles(int): Number of iterations to train.
        """
        self.cicles = cicles
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
        """ From key which key from the list are in a square neighborhood of vecinity length.

        Args:
            key (_type_): Key from training data.
            vecinity (int): Distance of the vecinity.
            list_keys (list): Key list to search in the vecinity.

        Returns:
            list: Key list in the vecinity.
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
        """ Creates a matrix with normalize weight vector.
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
        """ Graph the som weight matrix.

        Returns:
            plt.figure: Una figura de matplotlib.pyplot.figure.
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
            plt.figure
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
        """ Graph matrix the SOM weights matrix with a line between 2 BMU

        Args:
            v (list): Vector from key.
            u (list): Vector from key.

        Returns:
            plt.figure
        """
        fig=plt.figure()
        bmu_v = self.best_matching_unit(v) # Índice del la celula más parecida del vector v.
        bmu_u = self.best_matching_unit(u) # Índice del la celula más parecida del vector u.
        
        v_i,v_j = self.coor_from_index(bmu_v)
        
        u_i,u_j = self.coor_from_index(bmu_u)
        
        plt.pcolor(self.normsMatrix, cmap='jet_r')  # Mapa de calor de la distancia de las unidades
        plt.plot([u_i, v_i],[u_j, v_j],color='black')
        return fig, v_i, v_j, u_i, u_j, self.weights[bmu_v], self.weights[bmu_u]
    
    def coor_from_index(self, index:int) -> tuple:
        """ Get matrix coordinates from a list.

        Args:
            index (int): Index from the list

        Returns:
            tuple: Return (i,j) representing the index.
        """
        bmu_i = math.floor(index / self.n) # fila del bmu.
        bmu_j = index % self.n # columna del bmu.
        return (bmu_i,bmu_j)
    
    # ---------- Formato Json ---------- #
    
    # Guardar datos en formato json
    def save(self, nameSom:str, nameFile:str) -> None:
        """ Creates json file containing the SOM Instance.

        Args:
            nameSom(str): Name of the SOM.
            nameFile(str): File path to save.
        """
        self.jsonData['name'] = nameSom
        self.jsonData['n'] = self.n
        self.jsonData['training_iterations'] = self.training_i
        self.jsonData['training_rate'] = self.learning_rate
        self.jsonData['weights_length'] = self.weightsLen
        self.jsonData['weights'] = self.weights
        
        
        dm.saveJson(self.jsonData, nameFile)
                
# ----------Operaciones con vectores ----------#

# Norma para un vector.
def norm(x:list) -> float:
    """ Returns length of vector x.
    
    Args:
        x(list): Vector to normalize.

    Returns:
        float: Length of x.
    """
    sum = 0
    for i in range(len(x)):
        sum += x[i]**2
        
    return math.sqrt(sum)

# Distancia eucidiana para dos vectores.   
def dist_euclid(x:list, y:list) -> float:
    """ Returns euclid distance between vectors.

    Args:
        x(list): Vector.
        y(list): Vector.
    
    Returns:
        float: Euclid distance.
    """
    sum = 0
    if len(x)!=len(y):
        print(f"Error x:{len(x)}, y:{len(y)}")
    for i in range(len(x)):
        sum +=  (x[i] - y[i])**2
    return math.sqrt(sum)

# Distancia de manhattan para dos vectores. 
def dist_manhattan(x:list, y:list) -> int:
    """ Returns manhattan distance between 2 positions in the Matrix.

    Args:
        x(list): Vector 2d.
        y(list): Vector 2d.

    Returns:
        int: Manhattan distance.
    """
    sum = 0
    for i in range(len(x)):
        sum += abs(x[i] - y[i])
    return sum       

# Cosine similarity bweteen two vectors.
def cos_simi(x:list, y:list) -> float:
    """ Angle distance between vector.

    Args:
        x(list): Vector.
        y(list): Vector.

    Returns:
        float: Radians of Angle.
    """
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
