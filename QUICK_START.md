# 🚀 Quick Start - Sistema de Gestión de Alumnos

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Verificar MySQL
```bash
mysql.server status
# Si no está corriendo:
mysql.server start
```

### 2️⃣ Iniciar el Servidor
```bash
cd /Users/dru/Documents/Repositories/flask-alumno
source venv/bin/activate
python run.py
```

✅ **Servidor corriendo en**: http://localhost:5001

---

## 🧪 Probar la API (30 segundos)

### Opción 1: Usando curl
```bash
# 1. Obtener token
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. Guardar el token y usarlo
TOKEN="tu_token_aqui"

# 3. Listar cursos
curl http://localhost:5001/api/cursos/disponibles \
  -H "Authorization: Bearer $TOKEN"
```

### Opción 2: Script automático
```bash
bash test_endpoints.sh
```

---

## 📊 Para JMeter

### Archivos que necesitas:
1. **CSV de datos**: `data/alumnos_test.csv` (50 alumnos)
2. **Guía completa**: `JMETER_GUIDE.md`
3. **Colección Postman**: `postman_collection.json`

### Endpoints principales para testing:

| Endpoint | Propósito | Usuarios sugeridos |
|----------|-----------|-------------------|
| `POST /api/login` | Test CPU (hash) | 100 |
| `POST /api/alumno/registrar` | Test BD Write | 50 |
| `GET /api/cursos/estadisticas` | Test BD Read (JOIN) | 200 |
| `POST /api/simular-promedio` | Test CPU puro | 500 |

---

## 🛠️ Comandos Útiles

```bash
# Ver estadísticas de BD
bash scripts_utils.sh db-stats

# Reiniciar BD
bash scripts_utils.sh reset-db

# Generar más datos de prueba
bash scripts_utils.sh generate-data

# Limpiar tabla de alumnos
bash scripts_utils.sh clean-alumnos

# Ver ayuda completa
bash scripts_utils.sh help
```

---

## 📝 Credenciales

**Usuario de prueba:**
- Username: `admin`
- Password: `admin123`

**Base de datos:**
- Host: `localhost`
- User: `root`
- Password: `root`
- Database: `sistema_alumnos`

---

## 📚 Documentación

- **README.md** → Documentación completa
- **JMETER_GUIDE.md** → Guía para configurar JMeter
- **PROYECTO_COMPLETADO.md** → Resumen del proyecto
- **Este archivo** → Quick start

---

## 🎯 Para tu Test Plan

### 1. Configuración básica de JMeter:
- Instalar JMeter: `brew install jmeter` (macOS)
- Leer: `JMETER_GUIDE.md`
- Importar CSV: `data/alumnos_test.csv`

### 2. Crear 4 Thread Groups:
1. **Autenticación** (CPU-intensive)
2. **Registro Masivo** (BD Write)
3. **Consulta Pesada** (BD Read con JOIN)
4. **Cálculo en Memoria** (CPU puro)

### 3. Métricas a capturar:
- Throughput (requests/segundo)
- Response Time (promedio y percentiles)
- Error Rate (%)
- Latency

---

## ✅ Checklist

Antes de empezar con JMeter:

- [ ] MySQL corriendo (`mysql.server status`)
- [ ] Servidor Flask iniciado (puerto 5001)
- [ ] Token obtenido con `POST /api/login`
- [ ] CSV disponible en `data/alumnos_test.csv`
- [ ] JMeter instalado
- [ ] Documentación leída

---

## 🆘 Problemas Comunes

### Puerto 5001 ocupado
```bash
# Cambiar puerto en .env
PORT=5002

# O matar proceso
lsof -ti:5001 | xargs kill -9
```

### MySQL no conecta
```bash
# Verificar que MySQL esté corriendo
mysql.server start

# Verificar credenciales
mysql -u root -p
```

### Token expirado
```bash
# Obtener nuevo token
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

## 🎉 ¡Ya está todo listo!

Tu sistema está completamente configurado y listo para:
- ✅ Pruebas manuales
- ✅ Pruebas automatizadas
- ✅ Test Plan de JMeter
- ✅ Análisis de rendimiento

**¡Buena suerte con tu proyecto!** 🚀

---

**Próximo paso**: Lee `JMETER_GUIDE.md` para configurar tu Test Plan.
