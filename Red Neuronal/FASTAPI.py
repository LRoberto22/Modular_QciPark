import os
import numpy as np
import pandas as pd
import psycopg2
import random
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.utils import to_categorical
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Manejar los origenes que se permiten en el microservicio, ponienod la ip del servidor donde se aloja la página
origins = [
    "http://127.0.0.1:5500", 
]

# Permite acceso completo a los origenes especificados con anterioridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la base de datos PostgreSQL
conexion = psycopg2.connect(
    host="localhost",
    port="5432",
    database="modularbd",
    user="postgres",
    password="postgres"
)

# Cargar datos desde la base de datos
ingresos_data = pd.read_sql_query("SELECT * FROM ingresos", conexion)
egresos_data = pd.read_sql_query("SELECT * FROM egresos", conexion)
semana_data = pd.read_sql_query("SELECT * FROM dias_semana", conexion)

model_filename = "parking_model.h5"

# Función para cargar o crear el modelo
def load_or_create_model(input_shape, output_shape):
    if os.path.exists(model_filename):
        return load_model(model_filename)
    else:
        model = Sequential([
            Dense(128, activation='relu', input_shape=input_shape),
            Dense(output_shape, activation='linear')  
        ])
        model.save(model_filename)
        return model


# Función para preparar los datos
def prepare_data(ingresos_data, egresos_data, semana_data):
    best_parking_times = []

    # Iterar sobre cada día de la semana en semana_data
    for _, row in semana_data.iterrows():
        # Obtener el ID y nombre del día de la semana
        day_id = row['id_dia']
        day_name = row['dia']

        # Filtrar los datos de ingresos para el día específico
        ingresos_day = ingresos_data[ingresos_data['id_dia'] == day_id]
        
        # Filtrar los datos de egresos para el día específico
        egresos_day = egresos_data[egresos_data['id_dia'] == day_id]

        # Calcular la diferencia entre las horas de ingreso y egreso para cada registro
        parking_times = (egresos_day['horaegreso'] - ingresos_day['horaingreso']).dt.seconds / 3600


        # Seleccionar el mejor tiempo de estacionamiento (el más largo)
        best_parking_time = parking_times.max()
        
        # Guardar el mejor tiempo de estacionamiento para el día actual en la lista
        best_parking_times.append(best_parking_time)

    # Convertir a un array numpy
    X = np.array(best_parking_times)

    y = np.random.randint(50, size=len(semana_data))

    return X.reshape(-1, 1), y


# Preparar los datos
input_shape = (1,)  # Tamaño de las características de entrada
output_shape = 1  # Un solo valor de salida (mejor tiempo de estacionamiento)
X, y = prepare_data(ingresos_data, egresos_data, semana_data)

# Cargar o crear el modelo
model = load_or_create_model(input_shape, output_shape)

# Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(X, y, epochs=50, batch_size=32)

# Guardar el modelo entrenado
model.save(model_filename)


# Ruta de entrenamiento del modelo (POSTMAN)
@app.post("/train_model")
def train_model():

    return {"message": "Modelo entrenado correctamente"}

@app.get("/")
def index():
    return {"message": "Bienvenido al test de orientación vocacional"}




# Función para guardar en la base de datos
@app.post("/insertar_bd")
def insertar_base_datos(dato_que_mandaremos: str = Form(...), dato2: str = Form(...)):
    # Conectar a la base de datos y ejecutar la consulta
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO tabla_bd (nombre_columna_del_dato_a_ingresar, columna2) VALUES (%s, %s)"
        cursor.execute(query, (dato_que_mandaremos, dato2))
        conexion.commit()
        cursor.close()
    except Exception as e:
        return {"error": str(e)}
    
    return {"message": "Datos insertados correctamente"}



# Constructor y carga de microservicio
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)