import os
import numpy as np
import pandas as pd
import psycopg2
from datetime import datetime
from datetime import time, timedelta
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
        cursor.close()
        cursor.close()
    except Exception as e:
        return {"error": str(e)}
    

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

        cursor.close();
        if logeado:
            return{"existe": True, 'logeado': logeado}
        else:
            return{"existe": False}
    except Exception as e:
        return {"error": str(e)}
        

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
        if(horarioHoy == 0):
            return {horarioHoy}
        else:
            return {horarioHoy}
        
    except Exception as e:
        return {"error": str(e)}


# ---------------------------End point para usuario---------------------------
@app.post("/consultaHorario")
def consultaHorario(usr: int = Form(...)):
    try:
        cursor = conexion.cursor()
        query = f"select entrada, salida, fkdiasemana from horario_usuario where fkusuario = {usr};"
        cursor.execute(query)
        horario = cursor.fetchall()
        conexion.commit()
        cursor.close() 
        if(horario == 0):
            return [0]
        else:      
            return [horario]
    except Exception as e:
        return {"error": str(e)}
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

#---------------------------------------------------------RED NEURONAL---------------------------------------------#

# # Esta función se encarga de obtener los datos de la base de datos para un día específico. 
# #Toma un parámetro dia que representa el día de la semana para el que se desean los datos. 
# #Luego, ejecuta consultas SQL para obtener las horas de ingreso y de egreso correspondientes a ese día, convierte las horas 
# #de formato de cadena a objetos de tiempo, y devuelve dos DataFrames, uno para los ingresos y otro para los egresos.
# def obtener_datos_de_bd(dia: int):
#     cursor = conexion.cursor()

#     cursor.execute(f"SELECT hora_ingreso FROM ingresos WHERE fkdiasemana = {dia}")
#     ingresos_data = pd.DataFrame(cursor.fetchall(), columns=['hora_ingreso'])
#     ingresos_data['hora_ingreso'] = pd.to_datetime(ingresos_data['hora_ingreso'], format='%H:%M:%S').dt.hour

#     cursor.execute(f"SELECT hora_egreso FROM egresos WHERE fkdiasemana = {dia}")
#     egresos_data = pd.DataFrame(cursor.fetchall(), columns=['hora_egreso'])
#     egresos_data['hora_egreso'] = pd.to_datetime(egresos_data['hora_egreso'], format='%H:%M:%S').dt.hour

#     cursor.close()
#     return ingresos_data, egresos_data


# # Esta función se encarga de entrenar un modelo de red neuronal para predecir las horas pico de ingresos o egresos. 
# #Toma dos parámetros: X_train, que representa las características de entrada del modelo (en este caso, las horas del día como enteros), y y_train, que representa 
# #los valores objetivo del modelo (en este caso, la frecuencia de ingresos o egresos para cada hora del día). Utiliza un modelo de red neuronal con una capa oculta 
# #de 100 neuronas y una capa de salida lineal. El modelo se compila con la función de pérdida de error cuadrático medio y el optimizador Adam, y luego se entrena durante 100 épocas.
# def entrenar_red_neuronal(X_train, y_train):
#     model = Sequential()
#     model.add(Dense(100, input_dim=1, activation='relu'))
#     model.add(Dense(1))
#     model.compile(loss='mean_squared_error', optimizer='adam')
#     model.fit(X_train, y_train, epochs=100, batch_size=10, verbose=0)
#     return model

# #Esta función se encarga de calcular las horas pico de ingresos y egresos para un día específico utilizando un modelo de red neuronal. 
# #Primero, obtiene los datos de la base de datos llamando a obtener_datos_de_bd(dia). 
# #Luego, preprocesa los datos y entrena modelos de red neuronal para predecir las horas pico de ingresos y egresos utilizando la 
# #función entrenar_red_neuronal(X_train, y_train). Finalmente, hace predicciones utilizando los modelos entrenados y devuelve un diccionario con el día, 
# #la hora pico de ingresos y la hora pico de egresos.
# def calcular_horas_pico_y_actividad_con_red_neuronal(dia: int) -> dict:
#     ingresos_data, egresos_data = obtener_datos_de_bd(dia)

#     X_train = np.arange(24).reshape(-1, 1) 

#     y_ingresos = np.bincount(ingresos_data['hora_ingreso'], minlength=24)

#     ingresos_model = entrenar_red_neuronal(X_train, y_ingresos)

#     y_egresos = np.bincount(egresos_data['hora_egreso'], minlength=24)

#     egresos_model = entrenar_red_neuronal(X_train, y_egresos)

#     hora_pico_ingresos = ingresos_model.predict(np.array([[dia]]))[0][0]
#     hora_pico_egresos = egresos_model.predict(np.array([[dia]]))[0][0]

#     return {
#         "dia": dia,
#         "hora_pico_ingresos": hora_pico_ingresos,
#         "hora_pico_egresos": hora_pico_egresos
#     }

# # Función para calcular la hora menos activa antes de una hora especificada
# #utiliza una red neuronal para predecir la hora menos activa antes de la hora especificada. 
# #La hora devuelta es un valor numérico que representa la hora menos activa antes de la hora especificada. 
# #Luego, en el endpoint /hora_menos_actividad_antes/, convertimos este valor numérico de hora a formato de hora para devolverlo en la respuesta JSON.
# def calcular_hora_menos_actividad_antes_con_red_neuronal(dia: int, hora: time) -> str:
#     ingresos_data = obtener_datos_de_bd(dia)

#     # Preprocesamiento de datos
#     X_train = np.arange(24).reshape(-1, 1)  # Horas del día como enteros

#     # Convertir la hora especificada a un valor numérico entre 0 y 23
#     hora_num = hora.hour

#     # Entrenamiento del modelo
#     model = entrenar_red_neuronal(X_train, ingresos_data)

#     # Predicción de la hora menos activa antes de la hora especificada
#     hora_menos_activa_antes = model.predict(np.array([[hora_num]]))

#     return hora_menos_activa_antes[0][0]














#---------------------------------LÓGICA EMERGENCIA POR SI LA RED NEURONAL NO JALA CHIDO-----------------------------#
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
     hora_menos_actividad_ingresos = ingresos_data['hora_ingreso'][
         ingresos_data['hora_ingreso'] <= time(17, 0, 0)
     ].value_counts().idxmin() if not ingresos_data.empty else None

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


@app.get("/actividad_promedio_semanal/")
async def obtener_actividad_promedio_semanal():
     actividad_promedio = {}
    
     # Obtener el recuento de ingresos por día de la semana
     cursor.execute("SELECT fkdiasemana, COUNT(*) AS cantidad FROM ingresos GROUP BY fkdiasemana")
     resultados = cursor.fetchall()
    
     # Calcular el total de ingresos de la semana
     total_semana = sum(cantidad for _, cantidad in resultados)
    
     # Calcular el porcentaje de actividad para cada día de la semana
     for dia, cantidad in resultados:
         porcentaje_actividad = (cantidad / total_semana) * 100
         actividad_promedio[dia] = porcentaje_actividad
    
     return actividad_promedio



# Constructor y carga de microservicio
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)