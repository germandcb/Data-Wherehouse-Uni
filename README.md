# Proyecto Integrador 9 Semestre

## Descripción

Este proyecto implementa un data warehouse para el análisis de rendimiento académico en una universidad. Utiliza MySQL como base de datos relacional y sigue un modelo de estrella con tablas de dimensiones y una tabla de hechos para almacenar y consultar datos de estudiantes, carreras, sedes, materias, periodos académicos y rendimiento académico.

## Estructura del Proyecto

- `config/`: Contiene el archivo de dependencias.
  - `requirements.txt`: Lista de bibliotecas Python necesarias.
- `data/`: Archivos de datos fuente.
  - `Datos_limpios.xlsx`: Archivo Excel con datos de estudiantes y rendimiento académico.
  - `Dim_Carrera.csv`: Datos de carreras.
  - `Dim_Estudiante.csv`: Datos de estudiantes (aunque se usa el Excel).
  - `Dim_Materia.csv`: Datos de materias.
  - `Dim_Periodo.csv`: Datos de periodos académicos.
  - `Dim_Sede.csv`: Datos de sedes.
  - `Rendimiento_Academico.csv`: Datos de rendimiento (aunque se usa el Excel).
- `scripts/`: Scripts Python para la gestión del data warehouse.
  - `crear_data_warehouse.py`: Crea la base de datos y tablas en MySQL.
  - `cargar_datos_dw.py`: Carga los datos desde los archivos fuente a las tablas.
  - `verificar_tablas_dw.py`: Verifica la estructura y contenido de las tablas.

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

   Esto creará la base de datos "universidad" y las tablas necesarias.

2. Ejecuta el script para cargar los datos:

   ``` shell
   python scripts/cargar_datos_dw.py
   ```

   Esto insertará los datos desde los archivos CSV y Excel en las tablas correspondientes.

3. Opcionalmente, verifica las tablas:

   ``` shell
   python scripts/verificar_tablas_dw.py
   ```

## Notas

- Los scripts asumen que MySQL está configurado con usuario "root" y contraseña "root". Modifica las credenciales en los scripts si es necesario.
- Los archivos de datos deben estar en la carpeta `data/` relativa a los scripts.
- Asegúrate de que los archivos de datos no estén corruptos antes de ejecutar los scripts.
