import pandas as pd
import mysql.connector
import os
import logging
import datetime

# Crear directorio de logs si no existe
os.makedirs('logs', exist_ok=True)

# Configurar logging
logging.basicConfig(filename='logs/carga_datos.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def limpiar_datos_estudiantes(df):
    logging.info(f"Iniciando limpieza de {len(df)} registros de estudiantes")
    # Eliminar duplicados basados en ID_Estudiante
    df = df.drop_duplicates(subset=['ID_Estudiante'])
    # Eliminar duplicados basados en Cedula (mantener el primero)
    df = df.drop_duplicates(subset=['Cedula'])
    logging.info(f"Después de eliminar duplicados: {len(df)} registros")
    # Manejar valores nulos: eliminar filas con nulos en campos clave
    df = df.dropna(subset=['ID_Estudiante', 'Nombre_Completo', 'Cedula', 'Genero', 'Estrato_economico', 'Fecha_Nacimiento'])
    logging.info(f"Después de eliminar nulos: {len(df)} registros")
    # Normalización de texto
    df['Nombre_Completo'] = df['Nombre_Completo'].str.strip().str.title()
    df['Genero'] = df['Genero'].str.strip().str.upper()
    # Validación de formatos
    # Fechas: formato YYYY-MM-DD
    def validar_fecha(fecha):
        try:
            datetime.datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    df = df[df['Fecha_Nacimiento'].apply(validar_fecha)]
    logging.info(f"Después de validar fechas: {len(df)} registros")
    # Cédula: convertir a numérico, eliminar no válidas
    df['Cedula'] = pd.to_numeric(df['Cedula'], errors='coerce')
    df = df.dropna(subset=['Cedula'])
    df['Cedula'] = df['Cedula'].astype(int)
    logging.info(f"Después de validar cédulas: {len(df)} registros")
    # Género: solo M, F, OTRO
    df = df[df['Genero'].isin(['M', 'F', 'OTRO'])]
    logging.info(f"Después de validar géneros: {len(df)} registros")
    # Estrato económico: numérico, rango 1-6 (outliers)
    df['Estrato_economico'] = pd.to_numeric(df['Estrato_economico'], errors='coerce')
    df = df.dropna(subset=['Estrato_economico'])
    df = df[(df['Estrato_economico'] >= 1) & (df['Estrato_economico'] <= 6)]
    logging.info(f"Después de validar estratos y detectar outliers: {len(df)} registros")
    return df

def insertar_estudiantes(cursor, df):
    try:
        data = df[['ID_Estudiante', 'Nombre_Completo', 'Cedula', 'Genero', 'Estrato_economico', 'Fecha_Nacimiento']].values.tolist()
        logging.info(f"Preparando inserción de {len(data)} estudiantes")
        cursor.execute("START TRANSACTION")
        cursor.executemany("""
            INSERT INTO dim_estudiante
            (id_estudiante, nombre_completo, cedula, genero, estrato_economico, fecha_nacimiento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, data)
        cursor.execute("COMMIT")
        logging.info("Inserción de estudiantes completada exitosamente")
    except Exception as e:
        cursor.execute("ROLLBACK")
        logging.error(f"Error en inserción de estudiantes: {e}")
        raise

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
    csv_path = "data/Dim_Estudiante.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)
    logging.info(f"Leídos {len(df)} registros de estudiantes desde CSV")
    df_limpio = limpiar_datos_estudiantes(df)
    insertar_estudiantes(cursor, df_limpio)
    print("Datos de estudiantes cargados")

    # Obtener IDs de estudiantes válidos para filtrar hechos
    cursor.execute("SELECT id_estudiante FROM dim_estudiante")
    ids_estudiantes_validos = {row[0] for row in cursor.fetchall()}
    logging.info(f"IDs de estudiantes válidos: {len(ids_estudiantes_validos)}")

    # Datos de sedes
    csv_path = "data/Dim_Sede.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)
    logging.info(f"Leídos {len(df)} registros de sedes")
    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_sede
            (id_sede, nombre_sede, ciudad, direccion)
            VALUES (%s,%s,%s,%s)
        """, tuple(fila))
    logging.info("Datos de sedes cargados")
    print("Datos de sedes cargados")

    #Datos de Carreras
    csv_path = "data/Dim_Carrera.csv"
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
    csv_path = "data/Dim_Materia.csv"
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
    csv_path = "data/Dim_Periodo.csv"
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
    csv_path = "data/Dim_Becas.csv"
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
    csv_path = "data/Rendimiento_Academico.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")

    df = pd.read_csv(csv_path)
    logging.info(f"Leídos {len(df)} registros de rendimiento académico")

    # Filtrar solo registros con estudiantes válidos
    df = df[df['ID_Estudiante'].isin(ids_estudiantes_validos)]
    logging.info(f"Después de filtrar por estudiantes válidos: {len(df)} registros")

    for _, fila in df.iterrows():
        cursor.execute("""
            INSERT INTO rendimiento_academico
            (id_estudiante, id_materia, id_carrera, id_periodo, id_sede, id_beca, nota_final, aprobado, veces_cursada, jornada)
            VALUES (%s,%s,%s,%s,%s,NULL,%s,%s,%s,%s)
        """, tuple(fila))
    logging.info("Datos de rendimiento académico cargados")
    print("Datos de rendimiento academico cargados")

    conexion.commit()
    cursor.close()

except mysql.connector.Error as err:
    logging.error(f"Error de base de datos: {err}")
    print(f"Error de base de datos: {err}")
except FileNotFoundError as err:
    logging.error(f"Error de archivo: {err}")
    print(f"Error de archivo: {err}")
except Exception as err:
    logging.error(f"Error general: {err}")
    print(f"Error general: {err}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
    logging.info("Proceso de carga de datos finalizado")
