# 🎯 Guía de Configuración de JMeter

Esta guía te ayudará a configurar Apache JMeter para probar el Sistema de Gestión de Alumnos.

## 📥 Instalación de JMeter

### MacOS (Homebrew)
```bash
brew install jmeter
```

### Manual
1. Descargar desde: https://jmeter.apache.org/download_jmeter.cgi
2. Descomprimir y ejecutar: `bin/jmeter.sh` (Mac/Linux) o `bin/jmeter.bat` (Windows)

---

## 🧪 Test Plan Sugerido

### Estructura del Test Plan

```
Test Plan: Sistema de Gestión de Alumnos
├── Thread Group: 1. Autenticación (CPU-Intensive)
│   ├── HTTP Request Defaults
│   ├── HTTP Header Manager
│   ├── HTTP Request: POST /api/login
│   ├── JSON Extractor: token
│   └── Listeners (Summary Report, Graph Results)
│
├── Thread Group: 2. Registro Masivo (Escritura BD)
│   ├── CSV Data Set Config
│   ├── HTTP Request: POST /api/alumno/registrar
│   └── Listeners
│
├── Thread Group: 3. Consulta Pesada (Lectura BD)
│   ├── HTTP Request: GET /api/cursos/estadisticas
│   └── Listeners
│
└── Thread Group: 4. Cálculo en Memoria (CPU Puro)
    ├── HTTP Request: POST /api/simular-promedio
    └── Listeners
```

---

## 🔧 Configuración Detallada

### 1️⃣ Test de Autenticación (CPU-Intensive)

**Objetivo**: Medir la capacidad del servidor para verificar hashes SHA256 bajo carga.

#### Thread Group Configuration:
- **Number of Threads (users)**: 100
- **Ramp-Up Period (seconds)**: 10
- **Loop Count**: 50

#### HTTP Request Defaults:
- **Protocol**: http
- **Server Name or IP**: localhost
- **Port Number**: 5001

#### HTTP Header Manager:
```
Content-Type: application/json
```

#### HTTP Request: POST /api/login
- **Method**: POST
- **Path**: /api/login
- **Body Data**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

#### JSON Extractor (Extraer Token):
- **Name**: token
- **JSON Path**: $.token
- **Default Value**: TOKEN_NOT_FOUND

**Métricas a observar**:
- Throughput (requests/sec)
- Average Response Time
- CPU Usage del servidor

---

### 2️⃣ Test de Registro Masivo (Escritura BD)

**Objetivo**: Probar la capacidad de INSERT masivo en MySQL.

#### Thread Group Configuration:
- **Number of Threads**: 50
- **Ramp-Up Period**: 5
- **Loop Count**: 10

#### CSV Data Set Config:
- **Filename**: `${__BeanShell(import org.apache.jmeter.services.FileServer; FileServer.getFileServer().getBaseDir();)}/data/alumnos_test.csv`
  - O usar ruta absoluta: `/Users/dru/Documents/Repositories/flask-alumno/data/alumnos_test.csv`
- **File Encoding**: UTF-8
- **Variable Names**: `codigo,dni,nombre,apellido,email,telefono,fecha_ingreso`
- **Delimiter**: `,`
- **Recycle on EOF**: True
- **Stop thread on EOF**: False
- **Sharing mode**: All threads

#### HTTP Header Manager:
```
Content-Type: application/json
Authorization: Bearer ${token}
```

#### HTTP Request: POST /api/alumno/registrar
- **Method**: POST
- **Path**: /api/alumno/registrar
- **Body Data**:
```json
{
  "codigo": "${codigo}",
  "dni": "${dni}",
  "nombre": "${nombre}",
  "apellido": "${apellido}",
  "email": "${email}",
  "telefono": "${telefono}",
  "fecha_ingreso": "${fecha_ingreso}"
}
```

**Métricas a observar**:
- Throughput (INSERT/sec)
- Error Rate (DNI duplicados)
- Response Time
- Database Connection Pool

---

### 3️⃣ Test de Consulta Pesada (Lectura BD con JOINs)

**Objetivo**: Medir latencia en consultas con múltiples JOINs.

#### Thread Group Configuration:
- **Number of Threads**: 200
- **Ramp-Up Period**: 20
- **Loop Count**: 100

#### HTTP Request: GET /api/cursos/estadisticas
- **Method**: GET
- **Path**: /api/cursos/estadisticas

#### HTTP Header Manager:
```
Authorization: Bearer ${token}
```

**Métricas a observar**:
- Average Response Time
- 90th Percentile Response Time
- 95th Percentile Response Time
- Latency
- Database Query Time

---

### 4️⃣ Test de Cálculo en Memoria (CPU Puro)

**Objetivo**: Probar capacidad de procesamiento sin I/O de BD.

#### Thread Group Configuration:
- **Number of Threads**: 500
- **Ramp-Up Period**: 30
- **Loop Count**: 200

#### HTTP Request: POST /api/simular-promedio
- **Method**: POST
- **Path**: /api/simular-promedio

#### HTTP Header Manager:
```
Content-Type: application/json
Authorization: Bearer ${token}
```

#### Body Data:
```json
{
  "notas": [
    {"tipo": "Parcial 1", "nota": 15.5, "peso": 0.20},
    {"tipo": "Parcial 2", "nota": 17.0, "peso": 0.20},
    {"tipo": "Prácticas", "nota": 18.0, "peso": 0.30},
    {"tipo": "Final", "nota": 16.5, "peso": 0.30}
  ],
  "sistema": "20",
  "nota_minima_aprobacion": 10.5
}
```

**Métricas a observar**:
- Throughput máximo
- CPU Usage (debería estar al 100%)
- Response Time
- Memory Usage

---

## 📊 Listeners Recomendados

### 1. Summary Report
Muestra estadísticas básicas:
- Average, Min, Max
- Throughput
- Error %

### 2. View Results Tree
Para debugging, ver requests y responses individuales.

### 3. Aggregate Report
Estadísticas detalladas:
- 90%, 95%, 99% Percentiles
- Standard Deviation
- Error %

### 4. Response Time Graph
Visualización gráfica del tiempo de respuesta a lo largo del tiempo.

### 5. Active Threads Over Time
Visualiza cuántos threads están activos en cada momento.

### 6. Transactions per Second
Muestra el throughput en tiempo real.

---

## 🎯 Escenarios de Prueba Recomendados

### Escenario 1: Carga Normal
- **Usuarios**: 50 concurrentes
- **Duración**: 5 minutos
- **Objetivo**: Establecer baseline de rendimiento

### Escenario 2: Carga Pico
- **Usuarios**: 200 concurrentes
- **Duración**: 10 minutos
- **Objetivo**: Simular hora pico (matrículas)

### Escenario 3: Estrés
- **Usuarios**: 500+ concurrentes
- **Duración**: 15 minutos
- **Objetivo**: Encontrar el punto de quiebre

### Escenario 4: Resistencia (Soak Test)
- **Usuarios**: 100 concurrentes
- **Duración**: 1 hora
- **Objetivo**: Detectar memory leaks

---

## 🔍 Assertions Recomendadas

### Response Assertion:
```
Response Code: equals 200
```

### JSON Assertion:
```
$.success: equals true
```

### Duration Assertion:
```
Duration in milliseconds: < 1000
```

---

## 💡 Tips para Mejores Resultados

1. **Warm-up**: Ejecuta primero una ronda con pocos usuarios para "calentar" el servidor.

2. **Ramp-up**: No configures ramp-up = 0. Usa al menos 10-20% del total de usuarios.

3. **Monitoreo del Servidor**:
   ```bash
   # Ver CPU y Memoria
   top
   
   # Ver conexiones MySQL
   mysql -u root -p -e "SHOW PROCESSLIST;"
   
   # Ver logs de Flask
   tail -f logs/flask.log
   ```

4. **Limpieza entre Tests**:
   ```sql
   TRUNCATE TABLE alumnos;
   TRUNCATE TABLE matriculas;
   TRUNCATE TABLE notas;
   ```

5. **Resultados**:
   - Guarda los resultados en `.jtl` para análisis posterior
   - Compara diferentes configuraciones (CPU, memoria, pool de conexiones)

---

## 📈 Análisis de Resultados

### Métricas Clave:

| Métrica | Bueno | Aceptable | Malo |
|---------|-------|-----------|------|
| **Response Time (promedio)** | < 100ms | < 500ms | > 1000ms |
| **90th Percentile** | < 200ms | < 800ms | > 2000ms |
| **Error Rate** | < 0.1% | < 1% | > 5% |
| **Throughput** | Depende del hardware | - | - |
| **CPU Usage** | < 70% | < 85% | > 95% |

---

## 🚀 Optimizaciones Sugeridas

Si encuentras problemas de rendimiento:

### 1. Base de Datos:
- Agregar más índices
- Optimizar queries con `EXPLAIN`
- Aumentar `max_connections` en MySQL
- Configurar connection pooling

### 2. Servidor Flask:
- Usar Gunicorn con múltiples workers:
  ```bash
  gunicorn -w 4 -b 0.0.0.0:5001 run:app
  ```
- Habilitar caché (Redis)
- Usar CDN para assets estáticos

### 3. Sistema Operativo:
- Aumentar límite de file descriptors
- Optimizar TCP settings
- Agregar más RAM/CPU

---

## 📝 Ejemplo de Reporte

```
RESUMEN DEL TEST DE CARGA
========================

Test: Registro Masivo de Alumnos
Fecha: 3 de diciembre de 2025
Duración: 10 minutos

CONFIGURACIÓN:
- Usuarios concurrentes: 50
- Ramp-up: 5 segundos
- Total requests: 5000

RESULTADOS:
- Throughput: 125 req/sec
- Response Time (avg): 380ms
- Response Time (90%): 520ms
- Error Rate: 0.2%
- Total Errors: 10 (DNI duplicados)

CPU Usage: 65%
Memory Usage: 45%
DB Connections: 25/100

CONCLUSIÓN:
El sistema maneja bien 50 usuarios concurrentes.
Se recomienda probar con 100+ usuarios para encontrar límite.
```

---

¡Buena suerte con tus pruebas de carga! 🚀
