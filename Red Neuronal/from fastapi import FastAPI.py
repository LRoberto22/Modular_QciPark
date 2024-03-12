import os
import numpy as np
import pandas as pd
import psycopg2
from datetime import datetime
from datetime import time, timedelta
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.utils import to_categorical
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
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

# Definir una función para calcular la hora pico y la hora de menor actividad para un día específico
def calcular_horas_pico_y_actividad(dia: int) -> dict:
    cursor.execute(f"SELECT hora_ingreso FROM ingresos WHERE fkdiasemana = {dia}")
    ingresos_data = pd.DataFrame(cursor.fetchall(), columns=['hora_ingreso'])

    cursor.execute(f"SELECT hora_egreso FROM egresos WHERE fkdiasemana = {dia}")
    egresos_data = pd.DataFrame(cursor.fetchall(), columns=['hora_egreso'])

    # Convertir las horas a objetos time
    ingresos_data['hora_ingreso'] = pd.to_datetime(ingresos_data['hora_ingreso'], format='%H:%M:%S').dt.time
    egresos_data['hora_egreso'] = pd.to_datetime(egresos_data['hora_egreso'], format='%H:%M:%S').dt.time

    # Calcular la hora pico y la hora de menor actividad para ingresos
    hora_pico_ingresos = ingresos_data['hora_ingreso'].mode().iloc[0] if not ingresos_data.empty else None
    hora_menos_actividad_ingresos = ingresos_data['hora_ingreso'].value_counts().idxmin() if not ingresos_data.empty else None

    # Calcular la hora pico y la hora de menor actividad para egresos
    hora_pico_egresos = egresos_data['hora_egreso'].mode().iloc[0] if not egresos_data.empty else None
    hora_menos_actividad_egresos = egresos_data['hora_egreso'].value_counts().idxmin() if not egresos_data.empty else None

    return {
        "dia": dia,
        "hora_pico_ingresos": hora_pico_ingresos.strftime('%H:%M:%S') if hora_pico_ingresos else None,
        "hora_menos_actividad_ingresos": hora_menos_actividad_ingresos.strftime('%H:%M:%S') if hora_menos_actividad_ingresos else None,
        "hora_pico_egresos": hora_pico_egresos.strftime('%H:%M:%S') if hora_pico_egresos else None,
        "hora_menos_actividad_egresos": hora_menos_actividad_egresos.strftime('%H:%M:%S') if hora_menos_actividad_egresos else None
    }

@app.get("/horas_actividad/")
async def obtener_horas_actividad(dia: int):
    horas_actividad = calcular_horas_pico_y_actividad(dia)
    return horas_actividad

def calcular_hora_menos_actividad_antes(dia: int, hora: time):
    hora_ajustada = datetime.combine(datetime.today(), hora) - timedelta(minutes=15)
    hora_ajustada_str = hora_ajustada.strftime('%H:%M:%S')
    
    cursor.execute(f"SELECT hora_ingreso FROM ingresos WHERE fkdiasemana = {dia} AND hora_ingreso < '{hora}' ORDER BY hora_ingreso DESC")
    ingresos_data = pd.DataFrame(cursor.fetchall(), columns=['hora_ingreso'])
    
    if not ingresos_data.empty:
        hora_menos_actividad_antes = ingresos_data['hora_ingreso'].value_counts().idxmin()
    else:
        hora_menos_actividad_antes = hora_ajustada_str
    
    return hora_menos_actividad_antes

@app.get("/hora_menos_actividad_antes/")
async def obtener_hora_menos_actividad_antes(dia: int, hora: time):
    hora_menos_actividad_antes = calcular_hora_menos_actividad_antes(dia, hora)
    
    return {
        "dia": dia,
        "hora_especificada": hora.strftime('%H:%M:%S'),
        "hora_menos_actividad_antes": str(hora_menos_actividad_antes)
    }


# Constructor y carga de microservicio
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)