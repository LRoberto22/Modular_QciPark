import pandas as pd
import psycopg2

# Configuración de la conexión a la base de datos PostgreSQL
conexion = psycopg2.connect(
    host="modular-parking-modularparking.a.aivencloud.com",
    port="28916",
    database="defaultdb",
    user="avnadmin",
    password="AVNS_bJSJ3oB9EynJCouQhPY"
)

# Cargar datos desde la base de datos
cursor = conexion.cursor()

# Definir una función para calcular la hora pico y la hora de menor actividad para un día específico
def calcular_horas_pico_y_actividad(dia):
    cursor.execute(f"SELECT hora_ingreso FROM ingresos WHERE fkdiasemana = {dia}")
    ingresos_data = pd.DataFrame(cursor.fetchall(), columns=['hora_ingreso'])
    
    cursor.execute(f"SELECT hora_egreso FROM egresos WHERE fkdiasemana = {dia}")
    egresos_data = pd.DataFrame(cursor.fetchall(), columns=['hora_egreso'])
    
    # Convertir las horas a strings y luego a objetos datetime
    ingresos_data['hora_ingreso'] = pd.to_datetime(ingresos_data['hora_ingreso'].astype(str), format='%H:%M:%S').dt.hour
    egresos_data['hora_egreso'] = pd.to_datetime(egresos_data['hora_egreso'].astype(str), format='%H:%M:%S').dt.hour
    
    # Calcular la hora pico y la hora de menor actividad para ingresos
    hora_pico_ingresos = ingresos_data['hora_ingreso'].mode().iloc[0]
    hora_menos_actividad_ingresos = ingresos_data['hora_ingreso'].value_counts().idxmin()
    
    # Calcular la hora pico y la hora de menor actividad para egresos
    hora_pico_egresos = egresos_data['hora_egreso'].mode().iloc[0]
    hora_menos_actividad_egresos = egresos_data['hora_egreso'].value_counts().idxmin()
    
    return hora_pico_ingresos, hora_menos_actividad_ingresos, hora_pico_egresos, hora_menos_actividad_egresos

# Calcular para cada día de la semana
for dia in range(0, 6):  # Asumiendo que tienes datos para el día 0 y los días de la semana de 1 a 7
    hora_pico_ingresos, hora_menos_actividad_ingresos, hora_pico_egresos, hora_menos_actividad_egresos = calcular_horas_pico_y_actividad(dia)
    print(f"Dia {dia}")
    print("Ingresos - Hora pico:", hora_pico_ingresos)
    print("Ingresos - Hora de menor actividad:", hora_menos_actividad_ingresos)
    print("Egresos - Hora pico:", hora_pico_egresos)
    print("Egresos - Hora de menor actividad:", hora_menos_actividad_egresos)
    print("\n")
