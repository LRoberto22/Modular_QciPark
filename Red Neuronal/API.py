import os
import numpy as np
import pandas as pd
import psycopg2
from datetime import datetime
# from keras.models import Sequential, load_model
# from keras.layers import Dense
# from keras.utils import to_categorical
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
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
    host="modular-parking-modularparking.a.aivencloud.com",
    port="28916",
    database="defaultdb",
    user="avnadmin",
    password="VNS_bJSJ3oB9EynJCouQhPY"
)

@app.get("/obtener-usuario-horario/")
async def obtener_usuario_horario():
    try:
        # Obtener una sesión de la base de datos
        db = SessionLocal()

        # Ejecutar una consulta SQL directamente
        query = text("SELECT * FROM public.horario_usuario WHERE fkusuario = :usuario_id")
        result = db.execute(query, {"usuario_id": 216666666})
        horarios = result.fetchall()

        # Cerrar la sesión
        db.close()

        return {"horarios": horarios}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo horario del usuario: {str(e)}")


# @app.post("/ActualizacionHorario")
# def actualizaHorario():
#     db = conexion()
#     try:
#         fecha = datetime.now() 
#         query = f"CALL public.inserthorariousuario({fecha.strftime(f"%Y/%m/%d")}, {from.option_selected}, {from.option_selected}, {seteadoPorAhora}, );" 
#         db.execute(query)
#         db.commit()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error al ejecutar stored procedure: {str(e)}")
#     finally:
#         db.close()


#---------------Referencias API Mike--------------------
# # Cargar datos desde la base de datos
# preguntas_data = pd.read_sql_query("SELECT * FROM preguntas", conexion)
# pregunta_carrera_data = pd.read_sql_query("SELECT * FROM preguntas_carreras", conexion)
# carrera_data = pd.read_sql_query("SELECT * FROM carreras", conexion)


# # Ruta de entrenamiento del modelo (POSTMAN)
# @app.post("/train_model")
# def train_model():
    
#     return {"message": "Modelo entrenado correctamente"}

# @app.get("/")
# def index():
#     return {"message": "Bienvenido al test de orientación vocacional"}

# # Ruta para reiniciar la API
# @app.post("/reset_api")
# def reset():
    
#     return {"message": "Estado reiniciado"}


# # Ruta Para Mandar Respuesta
# @app.post("/submit_answer")
# def submit_answer(answer: int = Form(...), pregunta_id: int = Form(...)):
#    save_responses_to_database(dato_equis, dato_equis2)

#     return {"message": "Respuesta recibida"}



# # Función para guardar en la base de datos
# def save_responses_to_database(responses, carrera_recomendada):
#     # Crear una cadena de texto con los pares (idpregunta, respuesta)
#     response_text = ",".join(f"({pregunta_id}:{respuesta})" for pregunta_id, respuesta in responses)

#     cursor = conexion.cursor()

#     query = "INSERT INTO respuestas_usuario (respuestas, carrera_recomendada_id) VALUES (%s, %s)"
#     # Carga las respuestas y carrera a la base de datos
#     cursor.execute(query, (response_text, carrera_recomendada))
#     conexion.commit()
#     cursor.close()




#######################################
    


########################################
# Constructor y carga de microservicio
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)