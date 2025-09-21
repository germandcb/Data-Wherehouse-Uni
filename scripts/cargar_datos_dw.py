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
            INSERT IGNORE INTO dim_estudiante
            (id_estudiante, nombre_completo, cedula, genero, estrato_economico, fecha_nacimiento)
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
            (id_sede, nombre_sede, ciudad, direccion)
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
            (id_carrera, nombre_carrera, facultad, jornada_programa)
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
            (id_materia, nombre_materia, codigo_materia, numero_creditos)
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
            (id_periodo, codigo, anio, mes_inicio, mes_fin)
            VALUES (%s,%s,%s,%s,%s)
        """, tuple(fila))
    print("Datos de periodos cargados")

    #Datos de becas
    csv_path = "../data/Dim_Becas.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)

    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_becas
            (id_beca, nombre_beca, tipo_beca, monto_mensual)
            VALUES (%s,%s,%s,%s)
        """, tuple(fila))
    print("Datos de becas cargados")

    # Datos de la tabla de hechos
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Archivo no encontrado: {excel_path}")

    df = pd.read_excel(excel_path, sheet_name="Rendimiento_Academico")

    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO rendimiento_academico
            (id_estudiante, id_materia, id_carrera, id_periodo, id_sede, id_beca, nota_final, aprobado, veces_cursada, jornada)
            VALUES (%s,%s,%s,%s,%s,NULL,%s,%s,%s,%s)
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
