import csv
import json

def csv_read(csvFile:str) -> list:
    """ Reads CSV file with format key , vector with header
    Args:
        csvFile(str): File path to csv
    Returns:
        data(list): List of key:vector
    """
    data = []
    with open(csvFile) as file:
        reader = csv.reader(file)
        csv_data = list(reader)
        # Quitar los cabezales
        csv_data.pop(0)
            
        for i in csv_data:
            data.append([float(data) for data in i[1:]])
    return data

def csv_read_dict(csvFile:str) -> dict:
    """ Reads CSV file with format key , vector with header
    Args:
        csvFile(str): File path to csv
    Returns:
        data(dict): Dicionary with key, vector
    """
    data = {}
    with open(csvFile) as file:
        reader = csv.reader(file)
        csv_data = list(reader)
        # Quitar los cabezales
        csv_data.pop(0)
            
        for i in csv_data:
            data[i[0]] = [float(data) for data in i[1:]]
    return data

def csv_read_dict_woh(csvFile:str)->dict:
    """ Reads CSV file with format key, vector without header
    Args:
        csvFile(str): File path to csv file
    Returns:
        data(dict): Dictionary with key, vector data
    """
    data = {}
    with open(csvFile) as file:
        reader = csv.reader(file)
        csv_data = list(reader)
            
        for i in csv_data:
            data[i[0]] = [float(data) for data in i[1:]]
    return data

def getJson(add: str) -> dict:
    """ Reads JSON file to retrieve data.
    Args:
        add(str): File path to JSON file.
    Returns:
        somDict(dict): Dictionary represents SOM Instance.
    """
    with open(add, 'r') as f:
        somDict = json.load(f)
        
    return somDict

def saveJson(dic: dict, fileName: str) -> None:
    """ Saves dictionary representing SOM in File path.
    Args:
        dic(dict): Dictionaty represeting SOM
        fileName: File path to save the SOM instance
    """
    with open(fileName, 'w') as f:
        json.dump(dic, f)

