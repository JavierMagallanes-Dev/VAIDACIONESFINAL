# 🎓 Sistema de Gestión de Alumnos - API Flask + MySQL

Sistema de gestión académica diseñado para pruebas de rendimiento con JMeter. Incluye autenticación JWT, operaciones CRUD, consultas complejas con JOINs y cálculos en memoria.

## 📋 Características

- **Autenticación JWT**: Login con hash SHA256 (CPU-intensive para testing)
- **Registro Masivo**: Inserción de alumnos desde CSV
- **Consultas Pesadas**: JOINs múltiples para pruebas de latencia
- **Cálculos en Memoria**: Procesamiento de promedios sin I/O de BD
- **Base de Datos MySQL**: Esquema completo con índices optimizados

## 🛠️ Tecnologías

- Python 3.8+
- Flask 3.0
- MySQL 9.5 (Homebrew)
- PyMySQL
- JWT (PyJWT)
- Flask-CORS

## 📁 Estructura del Proyecto

```
flask-alumno/
├── app/
│   ├── __init__.py          # Configuración de Flask
│   ├── models/              # Modelos de datos
│   │   ├── alumno.py
│   │   ├── curso.py
│   │   └── usuario.py
│   ├── routes/              # Endpoints de la API
│   │   ├── auth.py          # POST /login
│   │   ├── alumno.py        # CRUD alumnos
│   │   ├── curso.py         # Consultas de cursos
│   │   └── calculo.py       # Cálculos en memoria
│   └── utils/               # Utilidades
│       ├── database.py      # Conexión MySQL
│       └── auth.py          # JWT helpers
├── data/
│   └── alumnos_test.csv     # 50 alumnos para JMeter
├── init_db.py               # Script de inicialización de BD
├── run.py                   # Punto de entrada
├── requirements.txt         # Dependencias Python
└── .env                     # Variables de entorno
```

## 🚀 Instalación y Configuración

### 1. Verificar MySQL

Tu MySQL ya está instalado y corriendo. Verifica:

```bash
mysql.server status
# Si está detenido:
mysql.server start
```

### 2. Clonar y Configurar el Proyecto

```bash
cd /Users/dru/Documents/Repositories/flask-alumno

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

El archivo `.env` ya está configurado con tus credenciales:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=sistema_alumnos
DB_PORT=3306

JWT_SECRET_KEY=tu_clave_secreta_muy_segura_cambiala_en_produccion

FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Inicializar la Base de Datos

```bash
python init_db.py
```

Este script:
- Crea la base de datos `sistema_alumnos`
- Crea las tablas: `usuarios`, `alumnos`, `cursos`, `matriculas`, `notas`
- Inserta un usuario de prueba: `admin` / `admin123`
- Inserta 5 cursos de ejemplo

### 5. Ejecutar el Servidor

```bash
python run.py
```

El servidor estará disponible en: `http://localhost:5000`

## 📡 Endpoints de la API

### 1. Autenticación (CPU-Intensive)

**POST** `/api/login`

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@sistema.com"
  }
}
```

**Para JMeter**: Usa este token en el header `Authorization: Bearer <token>` para los demás endpoints.

---

### 2. Registro Masivo de Alumnos (Escritura BD)

**POST** `/api/alumno/registrar`

**Headers**: `Authorization: Bearer <token>`

```json
{
  "codigo": "A20240001",
  "dni": "12345678",
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan@email.com",
  "telefono": "987654321",
  "fecha_ingreso": "2024-01-15"
}
```

**Para JMeter**: Usa el **CSV Data Set Config** con `data/alumnos_test.csv`:

```
CSV Data Set Config:
- Filename: data/alumnos_test.csv
- Variable Names: codigo,dni,nombre,apellido,email,telefono,fecha_ingreso
- Recycle on EOF: True
- Stop thread on EOF: False
```

Luego usa las variables en el Body JSON:
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

---

### 3. Consulta Pesada con JOINs (Lectura BD)

**GET** `/api/cursos/estadisticas`

**Headers**: `Authorization: Bearer <token>`

Esta consulta realiza:
- LEFT JOIN entre `cursos`, `matriculas` y `notas`
- Agregaciones con COUNT() y AVG()
- GROUP BY múltiple

**Ideal para medir latencia y tiempo de respuesta en JMeter.**

---

### 4. Historial de Alumno (JOIN Complejo)

**GET** `/api/historial/<alumno_id>`

**Headers**: `Authorization: Bearer <token>`

Ejemplo: `/api/historial/1`

Consulta que une 4 tablas: `alumnos` → `matriculas` → `cursos` → `notas`

---

### 5. Cálculo en Memoria (Procesamiento CPU)

**POST** `/api/simular-promedio`

**Headers**: `Authorization: Bearer <token>`

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

**Respuesta:**
```json
{
  "success": true,
  "resultado": {
    "promedio_simple": 16.75,
    "promedio_ponderado": 16.85,
    "nota_final": 17,
    "aprobado": true,
    "categoria": "Bueno",
    "detalles": {
      "cantidad_evaluaciones": 4,
      "nota_maxima": 18.0,
      "nota_minima": 15.5,
      "desviacion_estandar": 1.03
    }
  }
}
```

**Para JMeter**: Este endpoint NO accede a la BD, solo procesa en memoria. Ideal para:
- Probar capacidad de CPU
- Medir rendimiento sin cuellos de botella de I/O
- Escalar verticalmente (más CPU = mejor rendimiento)

---

### 6. Versión Simple (Sin Auth)

**POST** `/api/simular-promedio-simple`

**Sin autenticación**, para pruebas rápidas:

```json
{
  "notas": [15, 17, 18, 16]
}
```

---

## 🧪 Pruebas con JMeter

### Plan de Pruebas Sugerido

#### Test 1: Autenticación (CPU-Intensive)
- **Endpoint**: `POST /api/login`
- **Usuarios**: 100 usuarios concurrentes
- **Ramp-up**: 10 segundos
- **Loops**: 50
- **Objetivo**: Medir capacidad de verificación de hashes SHA256

#### Test 2: Escritura Masiva (BD)
- **Endpoint**: `POST /api/alumno/registrar`
- **CSV**: `data/alumnos_test.csv` (50 registros)
- **Usuarios**: 50 concurrentes
- **Objetivo**: Medir throughput de INSERTs en MySQL

#### Test 3: Consulta Pesada (BD con JOINs)
- **Endpoint**: `GET /api/cursos/estadisticas`
- **Usuarios**: 200 concurrentes
- **Objetivo**: Medir latencia de consultas con múltiples JOINs

#### Test 4: Cálculo en Memoria (CPU)
- **Endpoint**: `POST /api/simular-promedio`
- **Usuarios**: 500 concurrentes
- **Objetivo**: Medir capacidad de procesamiento sin I/O

### Configuración en JMeter

```
Thread Group:
├── HTTP Request Defaults
│   └── Server: localhost, Port: 5000
├── HTTP Header Manager
│   └── Content-Type: application/json
├── CSV Data Set Config (para Test 2)
├── HTTP Request (Login) → JSON Extractor (token)
├── HTTP Request (Endpoint a testear)
│   └── Authorization: Bearer ${token}
└── Listeners:
    ├── View Results Tree
    ├── Summary Report
    ├── Aggregate Report
    └── Response Time Graph
```

---

## 📊 Métricas a Evaluar en JMeter

| Métrica | Descripción |
|---------|-------------|
| **Throughput** | Transacciones por segundo |
| **Average Response Time** | Tiempo promedio de respuesta |
| **90th Percentile** | 90% de requests responden en este tiempo |
| **Error Rate** | Porcentaje de errores |
| **Latency** | Tiempo hasta el primer byte |

---

## 🔧 Comandos Útiles

### Base de Datos

```bash
# Conectar a MySQL
mysql -u root -p

# Ver bases de datos
SHOW DATABASES;

# Usar la base de datos
USE sistema_alumnos;

# Ver tablas
SHOW TABLES;

# Ver estructura de una tabla
DESCRIBE alumnos;

# Contar registros
SELECT COUNT(*) FROM alumnos;
```

### Python/Flask

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar nuevas dependencias
pip install <paquete>
pip freeze > requirements.txt

# Ejecutar servidor
python run.py

# Modo producción (Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## 📝 Notas para el Test Plan

1. **Orden de ejecución**:
   - Primero ejecuta `init_db.py` para tener datos iniciales
   - Luego ejecuta el servidor con `python run.py`
   - Finalmente configura y ejecuta tus pruebas en JMeter

2. **Token JWT**:
   - El token expira en 24 horas
   - Usa un **JSON Extractor** en JMeter para capturar el token del login
   - Pasa el token a los demás requests en el header `Authorization`

3. **CSV para Registro Masivo**:
   - El archivo `data/alumnos_test.csv` tiene 50 alumnos únicos
   - Configura `Recycle on EOF: True` para reutilizar el CSV
   - Los DNI y códigos son únicos (UNIQUE constraint en BD)

4. **Limpieza de Datos**:
   - Para limpiar la tabla de alumnos: `TRUNCATE TABLE alumnos;`
   - Para reiniciar todo: `python init_db.py` (DROP y CREATE)

---

## 🐛 Troubleshooting

### Error: "Access denied for user 'root'@'localhost'"
```bash
# Verificar credenciales en .env
# Conectar manualmente a MySQL para verificar:
mysql -u root -p
```

### Error: "Table doesn't exist"
```bash
# Ejecutar script de inicialización:
python init_db.py
```

### Error: "Port 5000 already in use"
```bash
# Cambiar puerto en .env o matar el proceso:
lsof -ti:5000 | xargs kill -9
```

### Error: "Module not found"
```bash
# Reinstalar dependencias:
pip install -r requirements.txt
```

---

## 📚 Recursos Adicionales

- [Documentación Flask](https://flask.palletsprojects.com/)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
- [JWT.io](https://jwt.io/)
- [JMeter User Manual](https://jmeter.apache.org/usermanual/index.html)

---

## 👨‍💻 Usuario de Prueba

**Username**: `admin`  
**Password**: `admin123`  
**Hash SHA256**: `240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9`

---

## 📄 Licencia

Este proyecto es para fines educativos y de testing.

---

¡Listo para JMeter! 🚀
