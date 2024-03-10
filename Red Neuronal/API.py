import os
import numpy as np
import pandas as pd
import psycopg2
from datetime import datetime
# from keras.models import Sequential, load_model
# from keras.layers import Dense
# from keras.utils import to_categorical
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

# ---------------------------End point para index (Simular un ingreso)---------------------------
@app.post("/insertarIngreso")
def insertarIngreso(fecha: str = Form(...), horaIngreso: str = Form(...), diaSemana: int = Form(...)):
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO ingresos (hora_ingreso, fecha, fkdiasemana) VALUES (%s, %s, %s)"
        cursor.execute(query, (horaIngreso, fecha, diaSemana))
        conexion.commit()
        cursor.close()
    except Exception as e:
        return {"error": str(e)}
    
    return {"message" : "Datos insertados correcamente"}

# ---------------------------End point para index (Simular un egreso)---------------------------
@app.post("/insertarEgreso")
def insertarIngreso(fecha: str = Form(...), horaEgreso: str = Form(...), diaSemana: int = Form(...)):
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO egresos (hora_egreso, fecha, fkdiasemana) VALUES (%s, %s, %s)"
        cursor.execute(query, (horaEgreso, fecha, diaSemana))
        conexion.commit()
        cursor.close()
    except Exception as e:
        return {"error": str(e)}
    
    return {"message" : "Datos insertados correcamente"}

# ---------------------------End point para index (Consultar el numero de cupos)---------------------------
@app.post("/consultaCupo")
def consultaCupo(fecha: str = Form(...), diaSemana: int = Form(...)):
    try:
        cursor = conexion.cursor()
        query = "SELECT COUNT(*) FROM ingresos WHERE fecha = %s AND fkdiasemana = %s"
        query2 = "SELECT COUNT(*) FROM egresos WHERE fecha = %s AND fkdiasemana = %s"
        cursor.execute(query, (fecha, diaSemana))
        ingresosRes = cursor.fetchone()[0]
        cursor.execute(query2, (fecha, diaSemana))
        egresoRes = cursor.fetchone()[0]
        conexion.commit()
        cursor.close()
    except Exception as e:
        return {"error": str(e)}
    
    return {egresoRes-ingresosRes}

# --------------------------- End point para Registro (Verificacion de usuarios existentes)----------------------------------------
@app.post("/verificarUsuario")
def verificar_usuario(codigoUsuario: int = Form(...)):
    try:
        cursor = conexion.cursor()
        query = "SELECT codigo FROM usuarios WHERE codigo = %s"
        cursor.execute(query, (codigoUsuario,))
        conexion.commit()
        usuario = cursor.fetchone()

        if usuario:
            return{"existe": True}
        else:
            return{"existe": False}

    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'cursor' in locals():
            cursor.close;

# ---------------------------End point para registro---------------------------
#Insercion en la base de datos en el registro de usuario
@app.post("/insertarUsuario_bd")
def insertar_usuario_bd(codigoUsuario: int = Form(...), nombreUsuario: str = Form(...), contrasenia: str = Form(...)):
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO usuarios (codigo, nombre, passw) VALUES (%s, %s, %s)"
        cursor.execute(query, (codigoUsuario, nombreUsuario, contrasenia))
        conexion.commit()
        cursor.close()

    except Exception as e:
        return {"error": str(e)}
    
    return {"message" : "Datos insertados correcamente"}
# ---------------------------End point para Login---------------------------
@app.post("/verificacionLogin")
def verificacionLogin(codigoUsuario: int = Form(...), contrasenia: str = Form(...)):
    try:
        cursor = conexion.cursor()
        query = "SELECT * FROM usuarios WHERE codigo = %s AND passw = %s"
        cursor.execute(query, (codigoUsuario, contrasenia))
        conexion.commit()
        logeado = cursor.fetchone()

        if logeado:
            return{"existe": True}
        else:
            return{"existe": False}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'cursor' in locals():
            cursor.close;

# ---------------------------End point para usuario----------------------------------------------- 
@app.post("/infoHorario")
def infoHorario(diaSemanaActual: int = Form(...), usuario: int = Form(...)):
    try:
        cursor = conexion.cursor()
        query = "select entrada, salida, dia from horario_usuario join dias_semana on fkdiasemana = id_dia where fkdiasemana = %s and fkusuario = %s;"
        cursor.execute(query, (diaSemanaActual, usuario))
        horarioHoy = cursor.fetchone()
        conexion.commit()
        cursor.close()        
    except Exception as e:
        return {"error": str(e)}
    return {horarioHoy}

# ---------------------------End point para usuario---------------------------
@app.post("/consultaHorario")
def consultaHorario(diaSemanaActual: str = Form(...)):

    try:
        cursor = conexion.cursor()
        query = "select entrada, salida, dia from horario_usuario join dias_semana on fkdiasemana = id_dia where fkdiasemana = %s and fkusuario = %s;"
        cursor.execute(query, (diaSemanaActual, usuario))
        horarioHoy = cursor.fetchone()
        conexion.commit()
        cursor.close()        
    except Exception as e:
        return {"error": str(e)}
    return {horarioHoy}


@app.post("/consultaHorario")
def consultaHorario(usr: str = Form(...)):
    try:
        cursor = conexion.cursor()
        query = "select entrada, salida, fkdiasemana from horario_usuario where fkusuario = %s;"
        cursor.execute(query, (usr,))
        horario = cursor.fetchall()
        conexion.commit()
        cursor.close()       
    except Exception as e:
        return {"error": str(e)}
    return [horario]
# ------------------------------End point para ingreso_horarios----------------------------------------------- 
@app.post("/enviarUsuarioHorario")
def guardarHorario(entrada: str = Form(...), salida: str = Form(...), codigoUsuario: int = Form(...), diaSemana: int = Form(...)):
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO horario_usuario (entrada, salida, fkusuario, fkdiasemana) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (entrada, salida, codigoUsuario, diaSemana))
        conexion.commit()
        cursor.close()
    except Exception as e:
        return {"error": str(e)}
    
    return {"Message: Insercion exitosa"}

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

# Constructor y carga de microservicio
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)