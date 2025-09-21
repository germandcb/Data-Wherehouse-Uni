import mysql.connector

try:
    # Conectar a MySQL (ajusta usuario, contraseña y host)
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conexion.cursor()

    # Crear base de datos
    cursor.execute("DROP DATABASE IF EXISTS universidad;")
    cursor.execute("CREATE DATABASE IF NOT EXISTS universidad;")
    cursor.execute("USE universidad;")

    # Crear tablas de dimensión
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_estudiante (
        ID_Estudiante INT AUTO_INCREMENT PRIMARY KEY,
        Nombre_Completo VARCHAR(100) NOT NULL,
        Cedula VARCHAR(20) UNIQUE,
        Genero VARCHAR(10),
        Estrato_economico INT,
        Fecha_Nacimiento DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_carrera (
        ID_Carrera INT AUTO_INCREMENT PRIMARY KEY,
        Nombre_Carrera VARCHAR(100) NOT NULL,
        Facultad VARCHAR(100),
        Jornada_Programa VARCHAR(50)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_sede (
        ID_Sede INT AUTO_INCREMENT PRIMARY KEY,
        Nombre_Sede VARCHAR(100) NOT NULL,
        Ciudad VARCHAR(100),
        Direccion VARCHAR(200)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_materia (
        ID_Materia INT AUTO_INCREMENT PRIMARY KEY,
        Nombre_Materia VARCHAR(100) NOT NULL,
        Codigo_Materia VARCHAR(20) UNIQUE,
        Numero_creditos INT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_periodo (
        ID_Periodo INT AUTO_INCREMENT PRIMARY KEY,
        Codigo VARCHAR(20) UNIQUE,
        Año INT,
        Mes_inicio INT,
        Mes_fin INT
    );
    """)

    # Crear tabla de hechos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rendimiento_academico (
        ID_Estudiante INT,
        ID_Materia INT,
        ID_Carrera INT,
        ID_Periodo INT,
        ID_Sede INT,
        Nota_Final DECIMAL(5,2),
        Aprobado BOOLEAN,
        Veces_Cursada INT,
        Jornada VARCHAR(50),
        FOREIGN KEY (ID_Estudiante) REFERENCES dim_estudiante(ID_Estudiante),
        FOREIGN KEY (ID_Materia) REFERENCES dim_materia(ID_Materia),
        FOREIGN KEY (ID_Carrera) REFERENCES dim_carrera(ID_Carrera),
        FOREIGN KEY (ID_Periodo) REFERENCES dim_periodo(ID_Periodo),
        FOREIGN KEY (ID_Sede) REFERENCES dim_sede(ID_Sede)
    );
    """)

    conexion.commit()
    cursor.close()
    print("Base de datos y tablas creadas con exito")

except mysql.connector.Error as err:
    print(f"Error en la creación de la base de datos: {err}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
