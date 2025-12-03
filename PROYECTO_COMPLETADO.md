# ✅ Proyecto Completado - Sistema de Gestión de Alumnos

## 🎉 Estado: LISTO PARA USAR

El proyecto Flask + MySQL está completamente configurado y funcionando.

---

## 📊 Resumen del Proyecto

### ✨ Características Implementadas

1. **✅ Autenticación JWT**
   - Endpoint: `POST /api/login`
   - Hash SHA256 para verificación (CPU-intensive)
   - Token con expiración de 24 horas

2. **✅ Registro Masivo de Alumnos**
   - Endpoint: `POST /api/alumno/registrar`
   - Validación de DNI y campos requeridos
   - CSV con 50 alumnos de prueba incluido

3. **✅ Consultas Pesadas con JOINs**
   - Endpoint: `GET /api/cursos/estadisticas`
   - Une 3 tablas: cursos + matrículas + notas
   - Agregaciones: COUNT, AVG

4. **✅ Historial Completo de Alumnos**
   - Endpoint: `GET /api/historial/<id>`
   - JOIN de 4 tablas
   - Información detallada de todos los cursos y notas

5. **✅ Cálculo en Memoria (CPU-intensive)**
   - Endpoint: `POST /api/simular-promedio`
   - Procesa promedios ponderados sin BD
   - Incluye cálculos estadísticos complejos

---

## 🗂️ Estructura del Proyecto

```
flask-alumno/
├── app/
│   ├── __init__.py              # Configuración Flask
│   ├── models/
│   │   ├── alumno.py           # Modelo Alumno
│   │   ├── curso.py            # Modelo Curso
│   │   └── usuario.py          # Modelo Usuario
│   ├── routes/
│   │   ├── auth.py             # Login (JWT)
│   │   ├── alumno.py           # CRUD Alumnos
│   │   ├── curso.py            # Consultas Cursos
│   │   └── calculo.py          # Cálculos en memoria
│   └── utils/
│       ├── database.py         # Conexión MySQL
│       └── auth.py             # JWT helpers
├── data/
│   └── alumnos_test.csv        # 50 alumnos para JMeter
├── init_db.py                  # Script inicialización BD
├── run.py                      # Punto de entrada
├── requirements.txt            # Dependencias
├── .env                        # Variables de entorno
├── .gitignore                  # Archivos ignorados
├── README.md                   # Documentación principal
├── JMETER_GUIDE.md            # Guía completa de JMeter
├── postman_collection.json     # Colección Postman
├── test_endpoints.sh          # Script pruebas bash
└── scripts_utils.sh           # Utilidades varias
```

---

## 🚀 Estado del Servidor

**✅ SERVIDOR CORRIENDO**

- **URL**: http://localhost:5001
- **Documentación**: http://localhost:5001/
- **Health Check**: http://localhost:5001/health
- **Puerto**: 5001 (configurado en .env)

### Usuario de Prueba:
- **Username**: `admin`
- **Password**: `admin123`

---

## 📡 Endpoints Disponibles

### Autenticación
- `POST /api/login` - Autenticación con JWT

### Alumnos
- `POST /api/alumno/registrar` - Registrar alumno
- `GET /api/alumnos` - Listar alumnos (paginado)
- `GET /api/alumno/<id>` - Obtener alumno por ID
- `GET /api/historial/<id>` - Historial completo (JOIN pesado)

### Cursos
- `GET /api/cursos/disponibles` - Listar cursos
- `GET /api/cursos/estadisticas` - Estadísticas con JOINs
- `GET /api/curso/<id>` - Obtener curso por ID

### Cálculos
- `POST /api/simular-promedio` - Cálculo ponderado (con auth)
- `POST /api/simular-promedio-simple` - Cálculo simple (sin auth)

### Utilidades
- `GET /health` - Health check
- `GET /` - Documentación de la API

---

## 🗄️ Base de Datos

**Estado**: ✅ INICIALIZADA Y FUNCIONANDO

### Tablas Creadas:
1. **usuarios** - Para autenticación (1 usuario de prueba)
2. **alumnos** - Registro de estudiantes
3. **cursos** - Catálogo de cursos (5 cursos de ejemplo)
4. **matriculas** - Relación alumno-curso
5. **notas** - Evaluaciones por matrícula

### Datos Iniciales:
- ✅ Usuario admin creado
- ✅ 5 cursos de ejemplo insertados
- ✅ Base de datos lista para recibir alumnos

---

## 🧪 Archivos de Prueba

### 1. CSV para JMeter
- **Archivo**: `data/alumnos_test.csv`
- **Contenido**: 50 alumnos únicos
- **Campos**: codigo, dni, nombre, apellido, email, telefono, fecha_ingreso
- **Uso**: Configurar en JMeter con CSV Data Set Config

### 2. Colección Postman
- **Archivo**: `postman_collection.json`
- **Importar en**: Postman o Insomnia
- **Incluye**: Todos los endpoints con ejemplos

### 3. Script de Pruebas
- **Archivo**: `test_endpoints.sh`
- **Ejecutar**: `bash test_endpoints.sh`
- **Prueba**: Todos los endpoints principales

---

## 🛠️ Scripts Útiles

### Script Principal: `scripts_utils.sh`

```bash
# Iniciar servidor
bash scripts_utils.sh start

# Reiniciar base de datos
bash scripts_utils.sh reset-db

# Ver estadísticas
bash scripts_utils.sh db-stats

# Ver últimos alumnos
bash scripts_utils.sh last-alumnos

# Generar más datos (150 alumnos)
bash scripts_utils.sh generate-data

# Crear backup
bash scripts_utils.sh backup

# Ver ayuda completa
bash scripts_utils.sh help
```

---

## 📚 Documentación Adicional

1. **README.md** - Documentación completa del proyecto
2. **JMETER_GUIDE.md** - Guía detallada para configurar JMeter
3. **postman_collection.json** - Para importar en Postman

---

## 🎯 Próximos Pasos Sugeridos

### 1. Probar Endpoints Manualmente
```bash
# Ejecutar script de pruebas
bash test_endpoints.sh
```

### 2. Importar en Postman
- Abrir Postman
- Importar `postman_collection.json`
- Configurar variable `{{token}}` después del login

### 3. Configurar JMeter
- Leer `JMETER_GUIDE.md`
- Crear Test Plan siguiendo la guía
- Usar `data/alumnos_test.csv` para registro masivo

### 4. Generar Más Datos
```bash
# Genera 150 alumnos adicionales
bash scripts_utils.sh generate-data
```

### 5. Monitorear Performance
```bash
# En una terminal separada
top

# O específicamente para Python
top | grep python
```

---

## 🔧 Comandos Rápidos

### Iniciar el Servidor
```bash
cd /Users/dru/Documents/Repositories/flask-alumno
source venv/bin/activate
python run.py
```

### Conectar a MySQL
```bash
mysql -u root -p
# Password: root
USE sistema_alumnos;
SHOW TABLES;
```

### Ver Estadísticas de BD
```bash
bash scripts_utils.sh db-stats
```

### Ejecutar Pruebas
```bash
bash test_endpoints.sh
```

---

## 📊 Tabla de Endpoints para JMeter

| Endpoint | Método | Tipo de Prueba | Objetivo |
|----------|--------|----------------|----------|
| `/api/login` | POST | CPU-Intensive | Hash SHA256 |
| `/api/alumno/registrar` | POST | DB Write | INSERT masivo |
| `/api/cursos/estadisticas` | GET | DB Read | JOIN pesado |
| `/api/historial/<id>` | GET | DB Read | JOIN 4 tablas |
| `/api/simular-promedio` | POST | CPU Puro | Sin I/O |

---

## ⚠️ Notas Importantes

1. **Puerto 5001**: El servidor está configurado en el puerto 5001 (5000 estaba ocupado)

2. **Entorno Virtual**: Siempre activar el venv antes de ejecutar scripts:
   ```bash
   source venv/bin/activate
   ```

3. **MySQL**: Debe estar corriendo antes de iniciar el servidor:
   ```bash
   mysql.server start
   ```

4. **Token JWT**: Expira en 24 horas. Obtener uno nuevo con `/api/login`

5. **DNI Únicos**: Los DNI tienen constraint UNIQUE. Para pruebas masivas, usar `scripts_utils.sh clean-alumnos`

---

## 🎓 Para tu Test Plan de JMeter

### Configuración Sugerida:

1. **Test 1: Autenticación**
   - 100 usuarios concurrentes
   - Ramp-up: 10s
   - Loops: 50
   - Métrica: CPU del servidor

2. **Test 2: Registro Masivo**
   - 50 usuarios concurrentes
   - CSV: `alumnos_test.csv`
   - Métrica: INSERT/segundo

3. **Test 3: Consulta Pesada**
   - 200 usuarios concurrentes
   - Endpoint: `/api/cursos/estadisticas`
   - Métrica: Latencia y Response Time

4. **Test 4: Cálculo Puro**
   - 500 usuarios concurrentes
   - Endpoint: `/api/simular-promedio`
   - Métrica: Throughput máximo

---

## ✅ Checklist de Verificación

- [x] Base de datos creada
- [x] Tablas inicializadas
- [x] Usuario de prueba creado
- [x] Cursos de ejemplo insertados
- [x] Servidor Flask funcionando
- [x] Endpoints respondiendo
- [x] CSV de prueba disponible
- [x] Documentación completa
- [x] Scripts de utilidades creados
- [x] Guía de JMeter documentada

---

## 🎉 ¡TODO LISTO!

El proyecto está completamente funcional y listo para:
- ✅ Pruebas manuales con Postman
- ✅ Pruebas automatizadas con bash scripts
- ✅ Pruebas de carga con JMeter
- ✅ Desarrollo adicional

**¡Éxito con tu Test Plan en JMeter!** 🚀

---

## 📞 Contacto y Soporte

Si necesitas ayuda:
1. Revisa `README.md` para documentación completa
2. Revisa `JMETER_GUIDE.md` para configuración de JMeter
3. Ejecuta `bash scripts_utils.sh help` para ver comandos disponibles

---

**Fecha de Creación**: 3 de diciembre de 2025
**Versión**: 1.0
**Estado**: Producción Lista ✅
