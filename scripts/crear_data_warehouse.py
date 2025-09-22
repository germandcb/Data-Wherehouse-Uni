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
        id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
        nombre_completo VARCHAR(100) NOT NULL,
        cedula VARCHAR(20) UNIQUE,
        genero VARCHAR(10),
        estrato_economico INT,
        fecha_nacimiento DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_carrera (
        id_carrera INT AUTO_INCREMENT PRIMARY KEY,
        nombre_carrera VARCHAR(100) NOT NULL,
        facultad VARCHAR(100),
        jornada_programa VARCHAR(50)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_sede (
        id_sede INT AUTO_INCREMENT PRIMARY KEY,
        nombre_sede VARCHAR(100) NOT NULL,
        ciudad VARCHAR(100),
        direccion VARCHAR(200)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_materia (
        id_materia INT AUTO_INCREMENT PRIMARY KEY,
        nombre_materia VARCHAR(100) NOT NULL,
        codigo_materia VARCHAR(20) UNIQUE,
        numero_creditos INT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_periodo (
        id_periodo INT AUTO_INCREMENT PRIMARY KEY,
        codigo VARCHAR(20) UNIQUE,
        anio INT,
        mes_inicio INT,
        mes_fin INT
    );
    """)


    # Crear tabla de hechos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rendimiento_academico (
        id_estudiante INT,
        id_materia INT,
        id_carrera INT,
        id_periodo INT,
        id_sede INT,
        nota_final DECIMAL(5,2),
        aprobado BOOLEAN,
        veces_cursada INT,
        jornada VARCHAR(50),
        FOREIGN KEY (id_estudiante) REFERENCES dim_estudiante(id_estudiante),
        FOREIGN KEY (id_materia) REFERENCES dim_materia(id_materia),
        FOREIGN KEY (id_carrera) REFERENCES dim_carrera(id_carrera),
        FOREIGN KEY (id_periodo) REFERENCES dim_periodo(id_periodo),
        FOREIGN KEY (id_sede) REFERENCES dim_sede(id_sede)
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
