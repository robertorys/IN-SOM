import json
import numpy as np
import pandas as pd
import random as rand
import math

#Checar la posibilidad de utilziar las librerias de numpy
#Implementación de miniSOM

class SOM:
    def __init__(self,nombre,n,muestra_poblacion,ciclos,tasa_de_aprendizaje=0.5):
        self.ciclos=ciclos
        self.nombre=nombre
        self.tasa_de_aprendizaje=tasa_de_aprendizaje
        self.weights=[]
        #Iniciar valores
    
    def header(self):# JSON del SOM
        return json.dumps(self)

    def ini_celulas(self,n,muestra_poblacion):# Generar la matriz de celulas inicial
        indexes=list(range(len(muestra_poblacion)))
        for i in range(n**2):
            indice = rand.randint(0,len(indexes))
            indexes.remove(indice)
            if i%n==0:
                self.weights.append([])
            self.weights[int(i/2)].append(muestra_poblacion[indice])##Le asigna un valor a la muestra.

    def training(self):#Funcion de entranamiento
        with open(self.fileTraining,'r') as train:
            lines=train.readlines()

    def dist_euclid(x,y):#Vectores
        res=0
        for i in range(len(x)):
            res+=(x-y)**2
        return math.sqrt(res)

    def best_matching_unit(self,entrada):
        best=None
        min=10000
        for i in self.weights:
            for j in i:
                if self.dist_euclid(j,entrada)<min:
                    best=j
        return best

    def SaveSOMState(self,direccion):#Guardar el som con formato json en la entrada
        with open(direccion,'w') as somsave:
            somsave.write(json.dump(self))

    def LoadSOMState(self,direccion):#Carga el SOM en formato json
        with open(direccion,'r') as somsave:
            json.loads(somsave.read())
            #Read json
            #  
    def Training(direccion):#Carga el CSV de entrenamiento
        with open(direccion,'r') as csvfile:
           values=csvfile.readlines()#Cada linea contiene un valor
           #Load CSV 