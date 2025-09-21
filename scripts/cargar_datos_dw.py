import pandas as pd
import mysql.connector
import os

try:
    # === Configuración conexión MySQL ===
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="universidad"
    )
    cursor = conexion.cursor()

    # Datos de estudiantes
    excel_path = "../data/Datos_limpios.xlsx"
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Archivo no encontrado: {excel_path}")

    df = pd.read_excel(excel_path, sheet_name="Dim_Estudiante")

    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_estudiante
            (ID_Estudiante, Nombre_Completo, Cedula, Genero, Estrato_economico, Fecha_Nacimiento)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, tuple(fila))
    print("Datos de estudiantes cargados")

    # Datos de sedes
    csv_path = "../data/Dim_Sede.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)

    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_sede
            (ID_Sede, Nombre_Sede, Ciudad, Direccion)
            VALUES (%s,%s,%s,%s)
        """, tuple(fila))
    print("Datos de sedes cargados")

    #Datos de Carreras
    csv_path = "../data/Dim_Carrera.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)

    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_carrera
            (ID_Carrera, Nombre_Carrera, Facultad, Jornada_Programa)
            VALUES (%s,%s,%s,%s)
        """, tuple(fila))
    print("Datos de carreras cargados")

    #Datos de materias
    csv_path = "../data/Dim_Materia.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)

    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_materia
            (ID_Materia, Nombre_Materia, Codigo_Materia, Numero_Creditos)
            VALUES (%s,%s,%s,%s)
        """, tuple(fila))
    print("Datos de materias cargados")

    #Datos de periodos
    csv_path = "../data/Dim_Periodo.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)

    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_periodo
            (ID_Periodo, Codigo, Año, Mes_inicio,Mes_fin)
            VALUES (%s,%s,%s,%s,%s)
        """, tuple(fila))
    print("Datos de periodos cargados")

    # Datos de la tabla de hechos
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Archivo no encontrado: {excel_path}")

    df = pd.read_excel(excel_path, sheet_name="Rendimiento_Academico")

    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO rendimiento_academico
            (ID_Estudiante, ID_Materia, ID_Carrera, ID_Periodo, ID_Sede, Nota_Final, Aprobado, Veces_Cursada, Jornada)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, tuple(fila))
    print("Datos de rendimiento academico cargados")

    conexion.commit()
    cursor.close()

except mysql.connector.Error as err:
    print(f"Error de base de datos: {err}")
except FileNotFoundError as err:
    print(f"Error de archivo: {err}")
except Exception as err:
    print(f"Error general: {err}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
