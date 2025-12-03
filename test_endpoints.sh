#!/bin/bash

# Script de prueba de endpoints
# Ejecutar: bash test_endpoints.sh

BASE_URL="http://localhost:5001"
TOKEN=""

echo "🧪 Probando Endpoints de la API"
echo "================================"
echo ""

# Test 1: Health Check
echo "1️⃣ Test: Health Check"
curl -s "$BASE_URL/health" | python3 -m json.tool
echo -e "\n"

# Test 2: Login
echo "2️⃣ Test: Login (Autenticación)"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}')
echo "$LOGIN_RESPONSE" | python3 -m json.tool

TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "❌ Error: No se pudo obtener el token"
    exit 1
fi

echo "✅ Token obtenido correctamente"
echo -e "\n"

# Test 3: Registrar Alumno
echo "3️⃣ Test: Registrar Alumno"
curl -s -X POST "$BASE_URL/api/alumno/registrar" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "codigo": "A99999",
    "dni": "99999999",
    "nombre": "Test",
    "apellido": "Usuario",
    "email": "test@email.com",
    "telefono": "999999999",
    "fecha_ingreso": "2024-12-03"
  }' | python3 -m json.tool
echo -e "\n"

# Test 4: Listar Cursos Disponibles
echo "4️⃣ Test: Cursos Disponibles"
curl -s -X GET "$BASE_URL/api/cursos/disponibles" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo -e "\n"

# Test 5: Estadísticas de Cursos (Consulta Pesada)
echo "5️⃣ Test: Estadísticas de Cursos (JOIN pesado)"
curl -s -X GET "$BASE_URL/api/cursos/estadisticas" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo -e "\n"

# Test 6: Cálculo de Promedio Simple
echo "6️⃣ Test: Cálculo de Promedio Simple (Sin Auth)"
curl -s -X POST "$BASE_URL/api/simular-promedio-simple" \
  -H "Content-Type: application/json" \
  -d '{"notas": [15, 17, 18, 16]}' | python3 -m json.tool
echo -e "\n"

# Test 7: Cálculo de Promedio Ponderado
echo "7️⃣ Test: Cálculo de Promedio Ponderado (CPU-intensive)"
curl -s -X POST "$BASE_URL/api/simular-promedio" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "notas": [
      {"tipo": "Parcial 1", "nota": 15.5, "peso": 0.20},
      {"tipo": "Parcial 2", "nota": 17.0, "peso": 0.20},
      {"tipo": "Prácticas", "nota": 18.0, "peso": 0.30},
      {"tipo": "Final", "nota": 16.5, "peso": 0.30}
    ],
    "sistema": "20",
    "nota_minima_aprobacion": 10.5
  }' | python3 -m json.tool
echo -e "\n"

echo "✅ Todas las pruebas completadas!"
