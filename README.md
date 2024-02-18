# IN-SOM

Implementación de una interfaz para un SOM, que muestra una representaión grafica del SOM. Junto con una modulo de python para trabajar con un SOM atraves de código sin el uso de la interfaz.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)

## Instalación

Asegúrate de tener Python 3.10.12 instalado. Descarga el repositorio y luego instala las dependencias.

Dependencias:
- matplotlib
- tkinter


Archivos:

-/IN-SOM
  - main.py #Archivo a ejecutar para tener la interfaz
  - /som
    - som.py #Archivo con la clase SOM y sus metodos
    - dataManager.py #Archivo que maneja la información json y csv
    - /data
      - sensorimotor.csv #Informacion para entrenar SOM Llave:[Valores]

## Uso

### Base de datos
Asegurate de que el archivo que tenga los datos de entrenamiento o consulta tenga cabezales y sea un formato csv.

Por ejemplo:

"Word","Auditory","Gustatory","Haptic"

"A",2.214,0,0.429

"ACAPPELLA",4.333,0,0.222

### Libreria SOM

Para entrenar un som con código tienes que importar somObject del modulo som, para después crear un objeto de la siguente forma:

```python
from som import somObject

N = 100 # Matrix size nxn.

som = somObject(N,'example.csv')

som.init_weights() # initialize weights with random values

cicles = 100 # number of training cycles

som.init_training()
```

Para buscar el BMU (Best Maching Unit) viene por defecto la distancia euclidina, pero si se desea modificar solo se tiene que ir al método best_matching_unit y modificar cual es método de selección.