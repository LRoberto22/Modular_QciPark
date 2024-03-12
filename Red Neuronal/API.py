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
            return{"existe": True, 'logeado': logeado}
        else:
            return{"existe": False}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'cursor' in locals():
            cursor.close;

# ---------------------------End point para usuario----------------------------------------------- 
@app.post("/getEntradaSalida")
def getEntradaSalida(diaSemanaActual: int = Form(...), usuario: int = Form(...)):
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
def consultaHorario(usr: int = Form(...)):
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


# Constructor y carga de microservicio
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)