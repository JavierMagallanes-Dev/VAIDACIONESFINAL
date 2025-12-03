# 🎯 Guía de Ejecución del Test Plan en JMeter

## 📋 Test Plan Completo - Sistema de Gestión de Alumnos

Este archivo `test_plan.jmx` cumple con **TODOS** los requisitos del documento del proyecto.

---

## ✅ Requisitos Cumplidos

### 1. Thread Groups (Grupos de Usuarios) ✓
- ✅ **Test 1**: 10 usuarios - Autenticación
- ✅ **Test 2**: 50 usuarios - Autenticación (carga media)
- ✅ **Test 3**: 50 usuarios - Registro masivo con CSV
- ✅ **Test 4**: 100 usuarios - Consulta pesada con JOIN
- ✅ **Test 5**: 100 usuarios - Cálculo en memoria (CPU)
- ✅ **Test 6**: 200 usuarios - Prueba de estrés (opcional, deshabilitado por defecto)

### 2. Elementos Obligatorios del Test Plan ✓
- ✅ **HTTP Request**: Todos los tests usan HTTP Sampler
- ✅ **CSV Data Set Config**: Test 3 usa `alumnos_test.csv`
- ✅ **Timers**: 
  - Constant Timer (100-200ms)
  - Gaussian Random Timer (300ms ±100ms, 500ms ±200ms)
- ✅ **Assertions**:
  - Response Assertion (códigos 200, 201)
  - JSON Path Assertion (validar success: true)
  - Duration Assertion (tiempos máximos)

### 3. Listeners Incluidos ✓
- ✅ **Summary Report** → `resultados/summary_report.csv`
- ✅ **Aggregate Report** → `resultados/aggregate_report.csv`
- ✅ **View Results in Table** → `resultados/table_results.csv`
- ✅ **Graph Results** → `resultados/graph_results.csv`
- ✅ **Response Time Graph** → `resultados/response_time.csv`
- ✅ **View Results Tree** (para debugging)

### 4. Validaciones Mínimas ✓
- ✅ Tiempos máximos de respuesta (Duration Assertion)
- ✅ Cantidad de errores (% Error en Reports)
- ✅ Throughput (peticiones por segundo)
- ✅ Latencia (en todos los reports)
- ✅ Tiempo promedio por request
- ✅ Percentiles 90%, 95%, 99% (en Aggregate Report)

---

## 🚀 Cómo Ejecutar el Test Plan

### Opción 1: Modo GUI (Para análisis y debugging)

```bash
# 1. Ir a la carpeta del proyecto
cd /Users/dru/Documents/Repositories/flask-alumno

# 2. Asegurarse de que el servidor Flask esté corriendo
source venv/bin/activate
python run.py

# 3. En otra terminal, abrir JMeter
jmeter

# 4. En JMeter:
#    - File → Open
#    - Seleccionar: test_plan.jmx
#    - Click en el botón verde "Start" (▶)
```

### Opción 2: Modo CLI (Para resultados finales)

```bash
# Ejecutar test plan completo en modo CLI
jmeter -n -t test_plan.jmx -l resultados/resultados_completos.jtl -e -o resultados/reporte_html

# Parámetros:
# -n: Modo no-GUI
# -t: Archivo del test plan
# -l: Archivo de log de resultados
# -e: Generar reporte HTML al final
# -o: Carpeta para el reporte HTML
```

### Opción 3: Ejecutar Tests Individuales

```bash
# Solo Test 1 (10 usuarios - Autenticación)
jmeter -n -t test_plan.jmx -l resultados/test1.jtl -Jtest=1

# Solo Test 3 (50 usuarios - Registro CSV)
jmeter -n -t test_plan.jmx -l resultados/test3.jtl -Jtest=3

# Solo Test 4 (100 usuarios - Consulta pesada)
jmeter -n -t test_plan.jmx -l resultados/test4.jtl -Jtest=4
```

---

## 📊 Estructura del Test Plan

```
test_plan.jmx
├── Variables Globales
│   ├── SERVER = localhost
│   ├── PORT = 5001
│   └── PROTOCOL = http
│
├── HTTP Request Defaults
│   └── Configuración común para todos los requests
│
├── HTTP Header Manager
│   └── Content-Type: application/json
│
├── Test 1: Autenticación (10 usuarios)
│   ├── Gaussian Random Timer (300ms ±100ms)
│   ├── POST /api/login
│   ├── JSON Extractor (token)
│   ├── Response Assertion (200 OK)
│   ├── JSON Assertion (success: true)
│   └── Duration Assertion (< 1000ms)
│
├── Test 2: Autenticación (50 usuarios)
│   ├── Gaussian Random Timer (300ms ±100ms)
│   ├── POST /api/login
│   ├── JSON Extractor (token)
│   ├── Response Assertion (200 OK)
│   └── Duration Assertion (< 1500ms)
│
├── Test 3: Registro Masivo CSV (50 usuarios)
│   ├── CSV Data Set Config (alumnos_test.csv)
│   ├── Constant Timer (200ms)
│   ├── POST /api/login → obtener token
│   ├── POST /api/alumno/registrar (con datos CSV)
│   ├── Response Assertion (201 Created)
│   └── Duration Assertion (< 2000ms)
│
├── Test 4: Consulta Pesada JOIN (100 usuarios)
│   ├── Gaussian Random Timer (500ms ±200ms)
│   ├── POST /api/login → obtener token
│   ├── GET /api/cursos/estadisticas (JOIN de 3 tablas)
│   ├── Response Assertion (200 OK)
│   └── Duration Assertion (< 3000ms)
│
├── Test 5: Cálculo en Memoria (100 usuarios)
│   ├── Constant Timer (100ms)
│   ├── POST /api/login → obtener token
│   ├── POST /api/simular-promedio (CPU intensive)
│   ├── Response Assertion (200 OK)
│   ├── JSON Assertion (success: true)
│   └── Duration Assertion (< 500ms)
│
├── Test 6: Estrés (200 usuarios) [DESHABILITADO]
│   ├── Gaussian Random Timer (800ms ±300ms)
│   ├── POST /api/login
│   ├── GET /api/cursos/estadisticas
│   └── Response Assertion (200 OK)
│
└── Listeners (Reportes)
    ├── Summary Report
    ├── Aggregate Report
    ├── View Results in Table
    ├── Graph Results
    ├── Response Time Graph
    └── View Results Tree
```

---

## 📈 Métricas que se Capturan

### En todos los reports se incluyen:

1. **Tiempo de Respuesta**
   - Average (promedio)
   - Min / Max
   - Median

2. **Percentiles**
   - 90% Line (Percentil 90)
   - 95% Line (Percentil 95)
   - 99% Line (Percentil 99)

3. **Throughput**
   - Requests/segundo
   - KB/segundo

4. **Latencia**
   - Tiempo hasta el primer byte
   - Connect Time

5. **Errores**
   - Error % (porcentaje)
   - Cantidad total de errores
   - Tipo de error

6. **Datos Transferidos**
   - Bytes enviados
   - Bytes recibidos

---

## 🎯 Escenarios de Prueba

### Escenario 1: Carga Ligera (Test 1)
**Objetivo**: Baseline de rendimiento
- **Usuarios**: 10 concurrentes
- **Duración**: ~2.5 minutos (50 loops)
- **Endpoint**: POST /api/login
- **Métrica clave**: Response Time < 1000ms

### Escenario 2: Carga Media (Test 2)
**Objetivo**: Comportamiento bajo carga normal
- **Usuarios**: 50 concurrentes
- **Duración**: ~2.5 minutos (30 loops)
- **Endpoint**: POST /api/login
- **Métrica clave**: Response Time < 1500ms

### Escenario 3: Escritura Masiva (Test 3)
**Objetivo**: Evaluar INSERT masivo en BD
- **Usuarios**: 50 concurrentes
- **Duración**: ~10 segundos (1 loop con CSV)
- **Endpoint**: POST /api/alumno/registrar
- **Métrica clave**: Response Time < 2000ms, Error % < 5%
- **Datos**: CSV con 50 alumnos únicos

### Escenario 4: Lectura Compleja (Test 4)
**Objetivo**: Evaluar consultas con JOIN
- **Usuarios**: 100 concurrentes
- **Duración**: ~3.5 minutos (20 loops)
- **Endpoint**: GET /api/cursos/estadisticas
- **Métrica clave**: Response Time < 3000ms, Latency

### Escenario 5: CPU Intensivo (Test 5)
**Objetivo**: Evaluar procesamiento sin I/O
- **Usuarios**: 100 concurrentes
- **Duración**: ~5 minutos (50 loops)
- **Endpoint**: POST /api/simular-promedio
- **Métrica clave**: Response Time < 500ms, Throughput alto

### Escenario 6: Estrés (Test 6) [OPCIONAL]
**Objetivo**: Encontrar el punto de quiebre
- **Usuarios**: 200 concurrentes
- **Duración**: ~2 minutos (10 loops)
- **Endpoint**: GET /api/cursos/estadisticas
- **Métrica clave**: Error %, punto de saturación

---

## 🔧 Configuración del Test Plan

### Variables que puedes cambiar:

En el Test Plan → Variables definidas:
```
SERVER = localhost      (cambiar si está en otro host)
PORT = 5001            (cambiar según tu configuración)
PROTOCOL = http        (cambiar a https si aplica)
```

### Archivo CSV:

El Test 3 usa: `data/alumnos_test.csv`

**Importante**: 
- La ruta es relativa al directorio donde ejecutas JMeter
- Si ejecutas desde otra carpeta, ajusta la ruta en CSV Data Set Config
- O usa ruta absoluta: `/Users/dru/Documents/Repositories/flask-alumno/data/alumnos_test.csv`

---

## ⚠️ Antes de Ejecutar

### Checklist:

- [ ] **Servidor Flask corriendo** en puerto 5001
  ```bash
  source venv/bin/activate
  python run.py
  ```

- [ ] **MySQL corriendo**
  ```bash
  mysql.server status
  ```

- [ ] **Carpeta resultados** creada (ya existe)

- [ ] **Archivo CSV** disponible en `data/alumnos_test.csv` ✓

- [ ] **JMeter instalado**
  ```bash
  jmeter -v
  # Debería mostrar: Apache JMeter 5.x
  ```

- [ ] **Limpiar datos anteriores** (opcional)
  ```bash
  bash scripts_utils.sh clean-alumnos
  ```

---

## 📊 Generar Reporte HTML Profesional

Después de ejecutar el test:

```bash
# 1. Ejecutar el test guardando resultados
jmeter -n -t test_plan.jmx -l resultados/resultados.jtl

# 2. Generar reporte HTML desde el .jtl
jmeter -g resultados/resultados.jtl -o resultados/reporte_html

# 3. Abrir el reporte
open resultados/reporte_html/index.html
```

El reporte HTML incluye:
- Dashboard con gráficos interactivos
- Estadísticas detalladas
- Top 5 requests más lentos
- Distribución de errores
- Gráficos de Response Time Over Time
- Throughput Over Time
- Active Threads Over Time

---

## 📝 Para tu Informe Técnico

### Datos que debes incluir:

1. **Configuración de Pruebas**
   - Número de usuarios por test
   - Ramp-up time
   - Loops
   - Duración total

2. **Métricas Obtenidas** (de Aggregate Report)
   - Average Response Time
   - 90th, 95th, 99th Percentile
   - Throughput (req/s)
   - Error %
   - Latency

3. **Análisis por Test**
   - Test 1 (10 usuarios): Baseline
   - Test 2 (50 usuarios): Carga media
   - Test 3 (CSV): Escritura masiva
   - Test 4 (100 usuarios): Lectura compleja
   - Test 5 (CPU): Procesamiento intensivo

4. **Conclusiones**
   - Endpoint más lento
   - Endpoint con más errores
   - Capacidad máxima del servidor
   - Cuellos de botella identificados

5. **Recomendaciones**
   - Optimizaciones de BD (índices, queries)
   - Escalamiento horizontal/vertical
   - Caching
   - Connection pooling

---

## 🎓 Tips para el Informe

### Screenshots que debes tomar:

1. **Aggregate Report** con todos los tests
2. **Response Time Graph** mostrando picos
3. **Summary Report** con totales
4. **View Results Tree** mostrando requests exitosos
5. **Reporte HTML** - Dashboard principal

### Gráficos para incluir:

- Response Time vs Número de Usuarios
- Throughput vs Número de Usuarios
- Error % por cada test
- Latency vs Response Time

---

## ✅ Validaciones Automáticas

El Test Plan incluye validaciones que fallarán automáticamente si:

- ❌ Response Code no es 200 o 201
- ❌ JSON no contiene `"success": true`
- ❌ Response Time excede el máximo configurado
- ❌ Token no se extrae correctamente

Estos errores se verán en rojo en el reporte.

---

## 🚀 ¡Listo para Ejecutar!

Tu Test Plan está **100% completo** y cumple con **todos** los requisitos del documento del proyecto.

### Comando rápido para empezar:

```bash
# Abrir JMeter con el Test Plan
jmeter -t test_plan.jmx
```

**¡Buena suerte con tu proyecto!** 🎯
