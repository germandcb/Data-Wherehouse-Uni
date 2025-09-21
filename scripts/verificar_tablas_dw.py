import mysql.connector

try:
    # Conectar a MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="universidad"
    )
    cursor = conexion.cursor()

    # Verificar tablas
    tablas = ["dim_estudiante", "dim_sede", "dim_carrera", "dim_materia", "dim_periodo", "rendimiento_academico"]
    for tabla in tablas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"Tabla {tabla}: {count} filas")
        except mysql.connector.Error as err:
            print(f"Error al consultar tabla {tabla}: {err}")

    cursor.close()

except mysql.connector.Error as err:
    print(f"Error de conexión: {err}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()