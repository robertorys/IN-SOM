# Datos de un objeto som:
# - Matriz de pesos.
# - Iteraciones para el entrenamiento.
# - Tasa de aprendizaje.
# - Datos de entrenamiento (dirección del csv)

from som import dataManager as dm
import matplotlib.pyplot as plt
import random
import math
from PIL import Image
import io

class somObject:
    normsMatrix = []

    # Iniciar el som nuevo.
    def __init__(self, n:int, cicles:int, training_data:str, somJson: str = None, learning_rate=0.5):
        self.strt = training_data
        self.dict_train_data=self.GetDict()
        self.training_data = dm.csv_read(self.strt)
        if not somJson:
            self.n = n
            self.cicles = cicles
            self.training_i = 0
            self.weightsLen = len(self.training_data[0])
            self.learning_rate = learning_rate
            self.weights = []
            self.dictData = {}
        else:
            self.dictData = dm.getJson(somJson)
            self.cicles = cicles
            self.n =  self.dictData['n']
            self.training_i = self.dictData['training_iterations']
            self.weightsLen = self.dictData['weights_length']
            self.learning_rate = learning_rate
            self.weights = self.dictData['weights']
            # self.normsMatrix = self.dictData['norms_matrix']
    
    # Regresa un muestreo de los datos de entrenamiento
    def get_sample(self) -> list:
        tdl = len(self.training_data)
        if tdl <= self.n:
            return self.training_data
        else:
            return random.sample(self.training_data, self.n)
    
    # Regresa el valor maximo y minimo de una muestra de los datos de entrenamiento.
    def get_max_min(self) -> list:
        sample = random.sample(self.training_data, self.n)
        max = 0
        min = 1000  
        max_i = self.weightsLen - 1
        
        for i in sample:
            i.sort()
            
            if max < i[max_i]:
                max = i[max_i]
                
            if min > i[0]:
                min = i[0]
        return min, max
                
    
    # Inicialización de la matriz de pesos.
    def init_weights(self):
        min, max = self.get_max_min()
        for i in range(self.n**2):
            w = []
            for j in range(self.weightsLen):
                w.append(round(random.uniform(min, max), 2))
            self.weights.append(w)
        self.createMatrixM()
    
    # Regresa en index de la mejor celula de la matriz de pesos.
    def best_matching_unit(self, x:list) -> int:
        min = 10000
        index = 0
        for w in self.weights:
            d = dist_euclid(x, w)
            if d < min:
                min = d
                bmu_i = index
            index += 1
                
        return bmu_i
        

    # Actualiza los pesos de una celula.
    def update_weight(self, bmu:list, w:list, lr_t:float) -> list:
        for i in range(len(w)):
            w[i] = w[i] + lr_t * (bmu[i] - w[i])  
        return w
            
    # Inicia el entrenamiento.
    def init_training(self):
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
            
            unique_sample = random.sample(self.training_data, 1)[0] # Obtener un dato para el entrenamiento.
            bmu = self.best_matching_unit(unique_sample) # Indice del la celula más parecida al dato para entrenamiento.

            
            # Actualización de los vecinos.
            # i / n = fila
            # i % n = columna
            
            bmu_i = math.floor(bmu / self.n) # fila del bmu.
            bum_j = bmu % self.n # columna del bmu.
            
            wi = 0
            for w in self.weights:
                wi_i = math.floor(wi / self.n) # fila del wi.
                wi_j = wi % self.n # columna del wi.
                
                if dist_manhattan([bmu_i, bum_j], [wi_i, wi_j]) < nr_t:
                    self.weights[wi] = self.update_weight(unique_sample, w, lr_t)
                wi += 1
            self.training_i += 1
            
            
            bmu = self.best_matching_unit(unique_sample) # Indice del la celula más parecida al dato para entrenamiento.

            if count == 100:
                print('cicles:', self.training_i)
                count = 0
            count += 1
        
        self.createMatrixM()
    
    def createMatrixM(self) -> None:
        self.normsMatrix = []
        index = 0
        for i in range(self.n):
            ni = []
            for j in range(self.n):
                ni.append(norm(self.weights[index]))
                index += 1
            self.normsMatrix.append(ni)
            
    def graph(self) -> None:
        self.createMatrixM()
        fig, axes = plt.subplots(1,1)
        plt.pcolor(self.normsMatrix, cmap='jet_r')  # Mapa de calor de la distancia de las unidades
        plt.colorbar()
        return fig
        
    
    def graphPoint(self, x:list):
        fig=plt.figure()
        bmu = self.best_matching_unit(x) # Indice del la celula más parecida al dato para entrenamiento.
        
        self.createMatrixM()
        
        bmu_i = math.floor(bmu / self.n) # fila del bmu.
        bmu_j = bmu % self.n # columna del bmu.
        plt.pcolor(self.normsMatrix, cmap='jet_r')  # Mapa de calor de la distancia de las unidades
        plt.plot(bmu_i,bmu_j,marker ="x",color='black')
        return fig, bmu_i, bmu_j
    
    def graphDif(self, v:list, u:list):
        fig=plt.figure()
        bmu_v = self.best_matching_unit(v) # Índice del la celula más parecida del vector v.
        bmu_u = self.best_matching_unit(u) # Índice del la celula más parecida del vector u.
        self.createMatrixM()
        
        v_i = math.floor(bmu_v/ self.n) # fila del bmu del vector v.
        v_j = bmu_v % self.n # columna del bmu del vector v.
        
        u_i = math.floor(bmu_u/ self.n) # fila del bmu del vector u.
        u_j = bmu_u % self.n # columna del bmu del vector u.
        
        plt.pcolor(self.normsMatrix, cmap='jet_r')  # Mapa de calor de la distancia de las unidades
        plt.plot([u_i, v_i],[u_j, v_j],color='black')
        return fig, v_i, v_j, u_i, u_j
    
    
    
    # ---------- Formato Json ---------- #
    
    # Guardar datos en formato json
    def save(self, nameSom:str, nameFile:str) -> None:
        
        self.dictData['name'] = nameSom
        self.dictData['n'] = self.n
        self.dictData['training_iterations'] = self.training_i
        self.dictData['training_rate'] = self.learning_rate
        self.dictData['weights_length'] = self.weightsLen
        self.dictData['weights'] = self.weights
        self.createMatrixM()
        self.dictData['norms_matrix'] = self.normsMatrix
        
        dm.saveJson(self.dictData, nameFile)

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