import os
import numpy as np
import pandas as pd
import psycopg2
from datetime import time, timedelta
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.utils import to_categorical
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pydantic import BaseModel
import tensorflow as tf
from keras.models import Sequential, load_model
from sklearn.neural_network import MLPRegressor
from datetime import datetime, timedelta, time
import json

#Librerias de prueba 
# from pydantic import BaseModel
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse

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
    host="modular-parking-modularparking.a.aivencloud.com",
    port="28916",
    database="defaultdb",
    user="avnadmin",
    password="AVNS_bJSJ3oB9EynJCouQhPY"
)



cursor = conexion.cursor()

def obtener_datos_de_bd(dia: int):
    cursor = conexion.cursor()

    cursor.execute(f"SELECT hora_ingreso FROM ingresos WHERE fkdiasemana = {dia}")
    ingresos_data = pd.DataFrame(cursor.fetchall(), columns=['hora_ingreso'])
    ingresos_data['hora_ingreso'] = pd.to_datetime(ingresos_data['hora_ingreso'], format='%H:%M:%S').dt.hour

    cursor.execute(f"SELECT hora_egreso FROM egresos WHERE fkdiasemana = {dia}")
    egresos_data = pd.DataFrame(cursor.fetchall(), columns=['hora_egreso'])
    egresos_data['hora_egreso'] = pd.to_datetime(egresos_data['hora_egreso'], format='%H:%M:%S').dt.hour

    cursor.close()
    return ingresos_data, egresos_data

def entrenar_red_neuronal(X_train, y_train):
    model = Sequential()
    model.add(Dense(100, input_dim=1, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_train, y_train, epochs=100, batch_size=10, verbose=0)
    return model

def calcular_horas_pico_y_actividad_con_red_neuronal(dia: int) -> dict:
    ingresos_data, egresos_data = obtener_datos_de_bd(dia)

    X_train = np.arange(24).reshape(-1, 1)  # Horas del día como enteros

    y_ingresos = np.bincount(ingresos_data['hora_ingreso'], minlength=24)

    ingresos_model = entrenar_red_neuronal(X_train, y_ingresos)

    y_egresos = np.bincount(egresos_data['hora_egreso'], minlength=24)

    egresos_model = entrenar_red_neuronal(X_train, y_egresos)

    hora_pico_ingresos = ingresos_model.predict(np.array([[dia]]))[0][0]
    hora_pico_egresos = egresos_model.predict(np.array([[dia]]))[0][0]

    return {
        "dia": dia,
        "hora_pico_ingresos": hora_pico_ingresos,
        "hora_pico_egresos": hora_pico_egresos
    }

@app.get("/horas_actividad/")
async def obtener_horas_actividad(dia: int):
    horas_actividad = calcular_horas_pico_y_actividad_con_red_neuronal(dia)
    horas_actividad_serializable = {
        "dia": horas_actividad["dia"],
        "hora_pico_ingresos": float(horas_actividad["hora_pico_ingresos"]),
        "hora_pico_egresos": float(horas_actividad["hora_pico_egresos"])
    }
    return horas_actividad_serializable


# Constructor y carga de microservicio
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)