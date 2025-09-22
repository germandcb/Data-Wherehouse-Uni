# Proyecto Integrador 9 Semestre

## Descripción

Este proyecto implementa un data warehouse para el análisis de rendimiento académico en una universidad. Utiliza MySQL como base de datos relacional y sigue un modelo de estrella con tablas de dimensiones y una tabla de hechos para almacenar y consultar datos de estudiantes, carreras, sedes, materias, periodos académicos y rendimiento académico.

## Estructura del Proyecto

- `config/`: Contiene el archivo de dependencias.
  - `requirements.txt`: Lista de bibliotecas Python necesarias (pandas, mysql-connector-python, openpyxl).
- `data/`: Archivos de datos fuente en formato CSV.
  - `Dim_Carrera.csv`: Datos de carreras.
  - `Dim_Estudiante.csv`: Datos de estudiantes.
  - `Dim_Materia.csv`: Datos de materias.
  - `Dim_Periodo.csv`: Datos de periodos académicos.
  - `Dim_Sede.csv`: Datos de sedes.
  - `Rendimiento_Academico.csv`: Datos de rendimiento académico.
- `logs/`: Directorio para archivos de log generados durante la carga de datos.
  - `carga_datos.log`: Registro de operaciones de limpieza y carga de datos.
- `scripts/`: Scripts Python para la gestión del data warehouse.
  - `crear_data_warehouse.py`: Crea la base de datos "universidad" y las tablas en MySQL.
  - `cargar_datos_dw.py`: Carga y limpia los datos desde los archivos CSV a las tablas, incluyendo validaciones y manejo de errores.
  - `verificar_tablas_dw.py`: Verifica la estructura y cuenta los registros en las tablas.

## Requisitos

- Python 3.x
- MySQL Server instalado y ejecutándose localmente.
- Usuario MySQL con permisos para crear bases de datos (por defecto: root/root).

## Instalación

1. Clona o descarga el proyecto.
2. Instala las dependencias de Python:

   ``` shell
   pip install -r config/requirements.txt
   ```

3. Asegúrate de que MySQL esté ejecutándose y accesible con las credenciales especificadas en los scripts (host="localhost", user="root", password="root").

## Ejecución

1. Ejecuta el script para crear el data warehouse:

    ``` shell
    python scripts/crear_data_warehouse.py
    ```

    Esto creará la base de datos "universidad" y las tablas necesarias, incluyendo dimensiones (estudiante, carrera, sede, materia, periodo) y la tabla de hechos (rendimiento_academico) con claves foráneas.

2. Ejecuta el script para cargar los datos:

    ``` shell
    python scripts/cargar_datos_dw.py
    ```

    Esto cargará y limpiará los datos desde los archivos CSV en `data/`, aplicando validaciones (eliminación de duplicados, manejo de nulos, normalización de texto, validación de formatos), y los insertará en las tablas correspondientes. Los logs de la operación se guardan en `logs/carga_datos.log`.

3. Opcionalmente, verifica las tablas:

    ``` shell
    python scripts/verificar_tablas_dw.py
    ```

    Esto mostrará el conteo de filas en cada tabla para confirmar la carga exitosa.

## Notas

- Los scripts asumen que MySQL está configurado con usuario "root" y contraseña "root". Modifica las credenciales en los scripts si es necesario.
- Los archivos de datos deben estar en la carpeta `data/` relativa a la raíz del proyecto.
- Asegúrate de que los archivos de datos no estén corruptos antes de ejecutar los scripts.
- Los logs de carga de datos se generan en `logs/carga_datos.log` para monitoreo y depuración.
- Una vez cargado el data warehouse, puedes proceder con análisis de datos. Consulta `analisis_preguntas_negocio.md` para ejemplos de consultas y preguntas de negocio.
