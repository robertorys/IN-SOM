import json
import numpy as np
import pandas as pd
class SOM:
    self.weights=[]
    def __init__(self,nombre,n,muestra_poblacion,ciclos,tasa_de_aprendizaje):
        self.ciclos=0
        self.nombre=
        for i in range(n):
            v=[]
            for j in range(n):
                v.append(0)
            weights.append(v)
    def header():# JSON del SOM

    def ini_celulas():# Generar la matriz de celulas inicial

    def training():#Funcion de entranamiento

    def best_matching_unit(entrada):

    def Save(self,direccion):#Guardar el som con formato json en la entrada
        with open(direccion,'w') as somsave:
            somsave.write(json.dump(self))
    def Load(self,direccion):#Carga el SOM en formato json
        with open(direccion,'r') as somsave:
            #Read json 
    def Training(direccion):#Carga el CSV de entrenamiento
        with open(direccion,'r') as csvfile:
            
