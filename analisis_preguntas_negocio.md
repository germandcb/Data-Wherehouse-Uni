# Análisis de Preguntas de Negocio en el Data Warehouse Universitario

Este documento explica las consultas SQL necesarias para responder las preguntas de negocio propuestas, basadas en el esquema del data warehouse. Incluye joins, agregaciones y filtros relevantes. Además, se analiza el esquema para sugerir preguntas adicionales importantes para el negocio.

## Esquema del Data Warehouse

- **dim_estudiante**: id_estudiante (PK), nombre_completo, cedula, genero, estrato_economico, fecha_nacimiento
- **dim_carrera**: id_carrera (PK), nombre_carrera, facultad, jornada_programa
- **dim_sede**: id_sede (PK), nombre_sede, ciudad, direccion
- **dim_materia**: id_materia (PK), nombre_materia, codigo_materia, numero_creditos
- **dim_periodo**: id_periodo (PK), codigo, anio, mes_inicio, mes_fin
- **dim_becas**: id_beca (PK), nombre_beca, tipo_beca, monto_mensual
- **rendimiento_academico**: id_estudiante (FK), id_materia (FK), id_carrera (FK), id_periodo (FK), id_sede (FK), id_beca (FK, opcional), nota_final, aprobado (BOOLEAN), veces_cursada, jornada

## Pregunta 1: ¿Qué materias tuvieron más estudiantes reprobados durante el 2024-2?

**Explicación**: Esta pregunta identifica materias con alto índice de reprobación, útil para mejorar la calidad educativa o asignar recursos adicionales.

**Consulta SQL**:

```sql
SELECT dm.nombre_materia, COUNT(DISTINCT ra.id_estudiante) AS estudiantes_reprobados
FROM rendimiento_academico ra
JOIN dim_materia dm ON ra.id_materia = dm.id_materia
JOIN dim_periodo dp ON ra.id_periodo = dp.id_periodo
WHERE dp.codigo = '2024-2' AND ra.aprobado = 0
GROUP BY dm.id_materia, dm.nombre_materia
ORDER BY estudiantes_reprobados DESC;
```

**Joins**: `rendimiento_academico` con `dim_materia` y `dim_periodo` para obtener nombres y filtrar periodo.
**Agregaciones**: COUNT DISTINCT de estudiantes reprobados por materia.
**Filtros**: Periodo '2024-2' y Aprobado = 0.

## Pregunta 2: ¿Cuál es la carrera que tuvo el mayor promedio en cálculo diferencial durante el 2024-2?

**Explicación**: Evalúa el rendimiento por carrera en una materia específica, ayudando a identificar fortalezas académicas.

**Asunción**: "Cálculo diferencial" se asume como "Matemáticas I" (ID_Materia correspondiente).

**Consulta SQL**:

```sql
SELECT dc.nombre_carrera, AVG(ra.nota_final) AS promedio
FROM rendimiento_academico ra
JOIN dim_carrera dc ON ra.id_carrera = dc.id_carrera
JOIN dim_materia dm ON ra.id_materia = dm.id_materia
JOIN dim_periodo dp ON ra.id_periodo = dp.id_periodo
WHERE dm.nombre_materia = 'Matemáticas I' AND dp.codigo = '2024-2'
GROUP BY dc.id_carrera, dc.nombre_carrera
ORDER BY promedio DESC
LIMIT 1;
```

**Joins**: Con `dim_carrera`, `dim_materia`, `dim_periodo`.
**Agregaciones**: AVG de Nota_Final por carrera.
**Filtros**: Materia específica y periodo.

## Pregunta 3: ¿Cuál es la carrera con más estudiantes matriculados durante el 2024-2?

**Explicación**: Muestra la popularidad de carreras, útil para planificación de recursos y admisiones.

**Consulta SQL**:

```sql
SELECT dc.nombre_carrera, COUNT(DISTINCT ra.id_estudiante) AS estudiantes_matriculados
FROM rendimiento_academico ra
JOIN dim_carrera dc ON ra.id_carrera = dc.id_carrera
JOIN dim_periodo dp ON ra.id_periodo = dp.id_periodo
WHERE dp.codigo = '2024-2'
GROUP BY dc.id_carrera, dc.nombre_carrera
ORDER BY estudiantes_matriculados DESC
LIMIT 1;
```

**Joins**: Con `dim_carrera` y `dim_periodo`.
**Agregaciones**: COUNT DISTINCT de estudiantes por carrera.
**Filtros**: Periodo '2024-2'.

## Pregunta 4: ¿Cuáles son los estudiantes que pueden aplicar para la beca por promedio académico en el 2025-1?

**Explicación**: Identifica candidatos a becas basados en criterios, promoviendo el mérito académico.

**Requisitos**: Promedio >= 4.0 en el último semestre (2024-2), no tener becas asignadas previamente.

**Consulta SQL**:

```sql
SELECT de.nombre_completo, AVG(ra.nota_final) AS promedio_ultimo_semestre
FROM rendimiento_academico ra
JOIN dim_estudiante de ON ra.id_estudiante = de.id_estudiante
JOIN dim_periodo dp ON ra.id_periodo = dp.id_periodo
WHERE dp.codigo = '2024-2'
  AND ra.id_beca IS NULL  -- No tienen beca asignada
GROUP BY de.id_estudiante, de.nombre_completo
HAVING AVG(ra.nota_final) >= 4.0
ORDER BY promedio_ultimo_semestre DESC;
```

**Joins**: Con `dim_estudiante` y `dim_periodo`.
**Agregaciones**: AVG por estudiante.
**Filtros**: Periodo, ID_Beca IS NULL, HAVING promedio >=4.0.
**Optimización**: ORDER BY para priorizar candidatos con mejor promedio.

## Preguntas Adicionales Sugeridas

1. **Tendencias de rendimiento académico**: ¿Cómo ha evolucionado el promedio general por periodo?
   - **Importancia**: Identifica mejoras o declives en la calidad educativa.
   - **Query**: `SELECT dp.codigo, AVG(ra.nota_final) FROM rendimiento_academico ra JOIN dim_periodo dp ON ra.id_periodo = dp.id_periodo GROUP BY dp.id_periodo ORDER BY dp.anio;`

2. **Retención estudiantil**: ¿Qué porcentaje de estudiantes repiten materias?
   - **Importancia**: Mide la efectividad de la enseñanza y apoyo estudiantil.
   - **Query**: `SELECT COUNT(DISTINCT CASE WHEN veces_cursada > 1 THEN id_estudiante END) / COUNT(DISTINCT id_estudiante) * 100 AS porcentaje_retencion FROM rendimiento_academico;`

3. **Impacto de becas en el rendimiento**: ¿Mejora el rendimiento de estudiantes con becas?
   - **Importancia**: Evalúa la efectividad de programas de becas.
   - **Query**: `SELECT db.tipo_beca, AVG(ra.nota_final) AS promedio_con_beca, COUNT(DISTINCT ra.id_estudiante) AS estudiantes FROM rendimiento_academico ra JOIN dim_becas db ON ra.id_beca = db.id_beca GROUP BY db.id_beca, db.tipo_beca ORDER BY promedio_con_beca DESC;`

4. **Rendimiento por estrato socioeconómico**: ¿Hay diferencias en el rendimiento por estrato?
   - **Importancia**: Identifica desigualdades y necesidades de apoyo.
   - **Query**: `SELECT de.estrato_economico, AVG(ra.nota_final) FROM rendimiento_academico ra JOIN dim_estudiante de ON ra.id_estudiante = de.id_estudiante GROUP BY de.estrato_economico;`

5. **Distribución de estudiantes por sede y carrera**: ¿Cómo se distribuyen los estudiantes?
   - **Importancia**: Ayuda en la planificación de infraestructura.
   - **Query**: `SELECT ds.nombre_sede, dc.nombre_carrera, COUNT(DISTINCT ra.id_estudiante) FROM rendimiento_academico ra JOIN dim_sede ds ON ra.id_sede = ds.id_sede JOIN dim_carrera dc ON ra.id_carrera = dc.id_carrera GROUP BY ds.id_sede, dc.id_carrera ORDER BY ds.nombre_sede, COUNT(DISTINCT ra.id_estudiante) DESC;`
