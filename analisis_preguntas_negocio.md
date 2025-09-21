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

## Pregunta 5: ¿Existen diferencias significativas en el rendimiento académico entre programas de jornada diurna y nocturna?

**Explicación**: Compara rendimiento por jornada, útil para ajustar horarios o programas.

**Consulta SQL**:

```sql
SELECT ra.jornada, AVG(ra.nota_final) AS promedio_rendimiento, COUNT(DISTINCT ra.id_estudiante) AS total_estudiantes
FROM rendimiento_academico ra
JOIN dim_periodo dp ON ra.id_periodo = dp.id_periodo
WHERE dp.anio >= 2022  -- Ejemplo para datos recientes
GROUP BY ra.jornada
ORDER BY promedio_rendimiento DESC;
```

**Joins**: Con `dim_periodo` para filtrar periodos.
**Agregaciones**: AVG y COUNT por jornada.
**Filtros**: Periodos recientes.

## Pregunta 6: ¿Cuál es la distribución de becas por carrera?

**Explicación**: Muestra qué carreras reciben más becas, útil para equilibrar oportunidades académicas.

**Consulta SQL**:

```sql
SELECT dc.nombre_carrera, COUNT(ra.id_estudiante) AS total_becas_asignadas
FROM rendimiento_academico ra
JOIN dim_carrera dc ON ra.id_carrera = dc.id_carrera
WHERE ra.id_beca IS NOT NULL
GROUP BY dc.id_carrera, dc.nombre_carrera
ORDER BY total_becas_asignadas DESC;
```

**Joins**: Con `dim_carrera`.
**Agregaciones**: COUNT de registros con beca por carrera.
**Filtros**: ID_Beca IS NOT NULL.

## Pregunta 7: ¿Cómo se distribuyen las becas por sede y período?

**Explicación**: Identifica patrones de asignación de becas por ubicación y tiempo, ayudando en la planificación regional.

**Consulta SQL**:

```sql
SELECT ds.nombre_sede, dp.codigo AS periodo, COUNT(ra.id_estudiante) AS total_becas
FROM rendimiento_academico ra
JOIN dim_sede ds ON ra.id_sede = ds.id_sede
JOIN dim_periodo dp ON ra.id_periodo = dp.id_periodo
WHERE ra.id_beca IS NOT NULL
GROUP BY ds.id_sede, ds.nombre_sede, dp.id_periodo, dp.codigo
ORDER BY dp.anio, dp.codigo, total_becas DESC;
```

**Joins**: Con `dim_sede` y `dim_periodo`.
**Agregaciones**: COUNT por sede y período.
**Filtros**: ID_Beca IS NOT NULL.
**Optimización**: ORDER BY para tendencias temporales.

## Pregunta 8: ¿Existe correlación entre tener beca y la tasa de aprobación?

**Explicación**: Evalúa si las becas influyen en el éxito académico, midiendo aprobaciones.

**Consulta SQL**:

```sql
SELECT
    CASE WHEN ra.id_beca IS NOT NULL THEN 'Con Beca' ELSE 'Sin Beca' END AS estado_beca,
    AVG(ra.nota_final) AS promedio_nota,
    SUM(CASE WHEN ra.aprobado = 1 THEN 1 ELSE 0 END) / COUNT(*) * 100 AS tasa_aprobacion,
    COUNT(DISTINCT ra.id_estudiante) AS total_estudiantes
FROM rendimiento_academico ra
GROUP BY CASE WHEN ra.id_beca IS NOT NULL THEN 'Con Beca' ELSE 'Sin Beca' END
ORDER BY tasa_aprobacion DESC;
```

**Agregaciones**: AVG nota, tasa aprobación (SUM aprobado / total), COUNT estudiantes.
**Filtros**: Ninguno, compara grupos.
**Optimización**: Usa CASE para categorizar.

## Pregunta 9: ¿Cuál es el impacto de diferentes tipos de beca en las notas finales?

**Explicación**: Compara el rendimiento académico por tipo de beca, optimizando asignaciones.

**Consulta SQL**:

```sql
SELECT db.tipo_beca, AVG(ra.nota_final) AS promedio_nota, COUNT(DISTINCT ra.id_estudiante) AS estudiantes_beneficiados
FROM rendimiento_academico ra
JOIN dim_becas db ON ra.id_beca = db.id_beca
GROUP BY db.id_beca, db.tipo_beca
ORDER BY promedio_nota DESC;
```

**Joins**: Con `dim_becas`.
**Agregaciones**: AVG nota, COUNT estudiantes por tipo.
**Filtros**: Solo registros con beca.

## Pregunta 10: ¿Qué carreras tienen mayor correlación entre becas y alto rendimiento?

**Explicación**: Identifica carreras donde las becas potencian mejor el rendimiento, guiando políticas.

**Consulta SQL**:

```sql
SELECT dc.nombre_carrera,
       AVG(CASE WHEN ra.id_beca IS NOT NULL THEN ra.nota_final END) AS promedio_con_beca,
       AVG(CASE WHEN ra.id_beca IS NULL THEN ra.nota_final END) AS promedio_sin_beca,
       (AVG(CASE WHEN ra.id_beca IS NOT NULL THEN ra.nota_final END) - AVG(CASE WHEN ra.id_beca IS NULL THEN ra.nota_final END)) AS diferencia
FROM rendimiento_academico ra
JOIN dim_carrera dc ON ra.id_carrera = dc.id_carrera
GROUP BY dc.id_carrera, dc.nombre_carrera
HAVING COUNT(CASE WHEN ra.id_beca IS NOT NULL THEN 1 END) > 0  -- Solo carreras con becas asignadas
ORDER BY diferencia DESC;
```

**Joins**: Con `dim_carrera`.
**Agregaciones**: AVG condicional para comparar promedios.
**Filtros**: HAVING para carreras con becas.

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

## Notas de Optimización para Consultas SQL

Para asegurar eficiencia en consultas, especialmente en tablas grandes:

- **Índices recomendados**: Crear índices en claves foráneas (ID_Estudiante, ID_Materia, etc.) y en campos frecuentemente filtrados como ID_Periodo.Codigo, ra.Aprobado.
- **Uso de DISTINCT**: Solo cuando necesario para evitar duplicados, como en conteos de estudiantes únicos.
- **Joins eficientes**: Usar INNER JOINs y evitar subqueries innecesarias; las consultas están diseñadas para joins directos.
- **Agregaciones**: GROUP BY con campos indexados; HAVING para filtros post-agregación.
- **ORDER BY**: Incluido para reportes claros, pero puede omitirse si no se necesita orden específico.
- **Filtros**: Aplicar WHERE temprano para reducir filas procesadas.

Estas optimizaciones permiten reportes rápidos y escalables en el data warehouse.
