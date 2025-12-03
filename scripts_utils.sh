#!/bin/bash

# Scripts Útiles para el Proyecto
# Ejecutar: bash scripts_utils.sh <comando>

case "$1" in
  
  # Iniciar el servidor
  "start")
    echo "🚀 Iniciando servidor Flask..."
    cd /Users/dru/Documents/Repositories/flask-alumno
    source venv/bin/activate
    python run.py
    ;;
  
  # Reiniciar la base de datos
  "reset-db")
    echo "🔄 Reiniciando base de datos..."
    cd /Users/dru/Documents/Repositories/flask-alumno
    source venv/bin/activate
    python init_db.py
    echo "✅ Base de datos reiniciada"
    ;;
  
  # Limpiar tabla de alumnos
  "clean-alumnos")
    echo "🧹 Limpiando tabla de alumnos..."
    mysql -u root -proot sistema_alumnos -e "TRUNCATE TABLE alumnos;"
    echo "✅ Tabla de alumnos limpia"
    ;;
  
  # Ver estadísticas de la BD
  "db-stats")
    echo "📊 Estadísticas de la Base de Datos"
    echo "===================================="
    mysql -u root -proot sistema_alumnos -e "
      SELECT 'Usuarios' as Tabla, COUNT(*) as Total FROM usuarios
      UNION ALL
      SELECT 'Alumnos', COUNT(*) FROM alumnos
      UNION ALL
      SELECT 'Cursos', COUNT(*) FROM cursos
      UNION ALL
      SELECT 'Matrículas', COUNT(*) FROM matriculas
      UNION ALL
      SELECT 'Notas', COUNT(*) FROM notas;
    "
    ;;
  
  # Ver últimos alumnos registrados
  "last-alumnos")
    echo "👥 Últimos 10 alumnos registrados:"
    mysql -u root -proot sistema_alumnos -e "
      SELECT id, codigo, dni, nombre, apellido, created_at
      FROM alumnos
      ORDER BY created_at DESC
      LIMIT 10;
    "
    ;;
  
  # Monitorear conexiones MySQL
  "mysql-connections")
    echo "🔍 Conexiones activas en MySQL:"
    mysql -u root -proot -e "SHOW PROCESSLIST;"
    ;;
  
  # Instalar dependencias
  "install")
    echo "📦 Instalando dependencias..."
    cd /Users/dru/Documents/Repositories/flask-alumno
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Dependencias instaladas"
    ;;
  
  # Ejecutar tests de endpoints
  "test")
    echo "🧪 Ejecutando tests de endpoints..."
    cd /Users/dru/Documents/Repositories/flask-alumno
    bash test_endpoints.sh
    ;;
  
  # Ver logs (si existen)
  "logs")
    echo "📋 Mostrando logs..."
    if [ -f "/Users/dru/Documents/Repositories/flask-alumno/logs/flask.log" ]; then
      tail -f /Users/dru/Documents/Repositories/flask-alumno/logs/flask.log
    else
      echo "No hay archivo de logs. El servidor muestra logs en consola."
    fi
    ;;
  
  # Generar más datos de prueba
  "generate-data")
    echo "🔢 Generando más datos de prueba..."
    python3 << 'EOF'
import csv
import random

nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Carmen", "Pedro", "Laura", "Miguel", "Isabel"]
apellidos = ["García", "Rodríguez", "Martínez", "López", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores"]

with open('/Users/dru/Documents/Repositories/flask-alumno/data/alumnos_extra.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['codigo', 'dni', 'nombre', 'apellido', 'email', 'telefono', 'fecha_ingreso'])
    
    for i in range(51, 201):  # Genera 150 alumnos más (del 51 al 200)
        codigo = f"A202400{i:02d}" if i < 100 else f"A2024{i:03d}"
        dni = f"{10000000 + i:08d}"
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        email = f"{nombre.lower()}.{apellido.lower()}{i}@email.com"
        telefono = f"98765{i:04d}"
        fecha = f"2024-02-{(i % 28) + 1:02d}"
        
        writer.writerow([codigo, dni, nombre, apellido, email, telefono, fecha])

print("✅ Archivo alumnos_extra.csv generado con 150 alumnos adicionales")
EOF
    ;;
  
  # Backup de la base de datos
  "backup")
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    echo "💾 Creando backup de la base de datos..."
    mysqldump -u root -proot sistema_alumnos > "/Users/dru/Documents/Repositories/flask-alumno/backup_${TIMESTAMP}.sql"
    echo "✅ Backup creado: backup_${TIMESTAMP}.sql"
    ;;
  
  # Restaurar backup
  "restore")
    if [ -z "$2" ]; then
      echo "❌ Error: Especifica el archivo de backup"
      echo "Uso: bash scripts_utils.sh restore <archivo.sql>"
      exit 1
    fi
    echo "📥 Restaurando backup: $2"
    mysql -u root -proot sistema_alumnos < "$2"
    echo "✅ Backup restaurado"
    ;;
  
  # Ayuda
  "help"|*)
    echo "🛠️  Scripts Útiles - Sistema de Gestión de Alumnos"
    echo "=================================================="
    echo ""
    echo "Uso: bash scripts_utils.sh <comando>"
    echo ""
    echo "Comandos disponibles:"
    echo "  start              - Iniciar el servidor Flask"
    echo "  reset-db           - Reiniciar la base de datos (DROP & CREATE)"
    echo "  clean-alumnos      - Limpiar tabla de alumnos (TRUNCATE)"
    echo "  db-stats           - Ver estadísticas de la BD"
    echo "  last-alumnos       - Ver últimos 10 alumnos registrados"
    echo "  mysql-connections  - Ver conexiones activas en MySQL"
    echo "  install            - Instalar/actualizar dependencias"
    echo "  test               - Ejecutar tests de endpoints"
    echo "  logs               - Ver logs del servidor"
    echo "  generate-data      - Generar más datos de prueba (150 alumnos)"
    echo "  backup             - Crear backup de la BD"
    echo "  restore <archivo>  - Restaurar backup"
    echo "  help               - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  bash scripts_utils.sh start"
    echo "  bash scripts_utils.sh reset-db"
    echo "  bash scripts_utils.sh generate-data"
    echo ""
    ;;
esac
