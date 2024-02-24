# IN-SOM

Implementation of an interface for a SOM, which shows a graphical representation of the SOM. Along with a python module to work with a SOM through code without the use of the interface.

## Content Table

- [Instalation](#instalation)
- [Use](#use)

## Instalation

Make sure you have Python 3.10.12 installed. Download the repository and then install the dependencies.

Dependecies:

- matplotlib
- tkinter

Files:

-/IN-SOM

- main.py #File that executes the interface
- /som
  - som.py #File that handles SOM class
  - dataManager.py #File that handles data retribution from CSV and Json files
  - /data
    - sensorimotor.csv #Training information for SOM[Valores]

## Use

### Data Base

Please make sure the file that contains the training data has headers and its in a csv format.

For example:

"Word","Auditory","Gustatory","Haptic" #Headers

"A",2.214,0,0.429 #Content

"ACAPPELLA",4.333,0,0.222 #Content

### Libreria SOM

For training a SOM without the interface, you need to import somObjet from de file SOM, for creating an instance of the SOM:

```python
from som import somObject

N = 100 # Matrix size nxn.

som = somObject(N,'example.csv')

som.init_weights() # initialize weights with random values

cicles = 100 # number of training cycles

som.init_training()
```

For searching the BMU (Best Matching Unit) the method used for defect is euclid distance, but if you want to modify it you only need to go to the methods 'best_matching_unit' and modify which is the selection method.
