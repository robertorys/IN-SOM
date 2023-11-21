import csv
import json

def csv_read(csvFile) -> list:
    data = []
    with open(csvFile) as file:
        reader = csv.reader(file)
        csv_data = list(reader)
        # Quitar los cabezales
        csv_data.pop(0)
            
        for i in csv_data:
            data.append([float(data) for data in i[1:]])
    return data

def csv_read_dict(csvFile) -> dict:
    data = {}
    with open(csvFile) as file:
        reader = csv.reader(file)
        csv_data = list(reader)
        # Quitar los cabezales
        csv_data.pop(0)
            
        for i in csv_data:
            data[i[0]] = [float(data) for data in i[1:]]
    return data

def csv_read_dict_woh(csvFile)->dict:
    data = {}
    with open(csvFile) as file:
        reader = csv.reader(file)
        csv_data = list(reader)
            
        for i in csv_data:
            data[i[0]] = [float(data) for data in i[1:]]
    return data

def getJson(add: str) -> dict:
    with open(add, 'r') as f:
        somDict = json.load(f)
        
    return somDict

def saveJson(dic: dict, fileName: str) -> None:
    with open(fileName, 'w') as f:
        json.dump(dic, f)

def txt_read(txtFile)->list:
    data=[]
    with open(txtFile,'r') as f:
        