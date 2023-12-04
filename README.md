# IN-SOM
Implementación de una interfaz para un SOM, que muestra una representaión grafica del SOM.

## Instalación

Asegúrate de tener Python instalado. Clona el repositorio y luego instala las dependencias.

```bash
git clone [https://github.com/tu_usuario/tu_proyecto.git](https://github.com/robertorys/IN-SOM.git)
cd IN-SOM
pip install -r requirements.txt
```
/IN-SOM
  ├── main.py #Archivo a ejecutar para tener la interfaz
  └── /som
    ├── som.py #Archivo con la clase SOM y sus metodos
    ├── dataManager.py #Archivo que maneja la información json y csv 
    ├── formato.txt #Formato del json creado por SOM
    ├── test.py #Prueba de SOM con sensorimotor.csv y guardado de SOM
    ├── testp.py #Prueba de graficacion con SOM
    ├── som_test_1_100x100.json #Som Entrenado
    └── /data
        ├── agrupamiento_test.csv #Archivo de practica para agrupamiento
        ├── agrupamiento_test_res #Archivo con resultados de agrupamiento
        ├── s.py #SOM Entrenado
        └── sensorimotor.csv #Informacion para entrenar SOM Llave:[Valores]
