# 🎨 Interfaz de Usuario - Sistema de Gestión de Alumnos

## ✨ Características de la UI

La interfaz web es **simple, minimalista y responsive**, diseñada con HTML, CSS y JavaScript vanilla (sin frameworks).

---

## 🖥️ Acceso a la Interfaz

**URL Principal**: http://localhost:5001

### Credenciales de Acceso:
- **Usuario**: `admin`
- **Contraseña**: `admin123`

---

## 📱 Pantallas Disponibles

### 1. **Login** (`/`)
- Autenticación con JWT
- Validación de credenciales
- Almacenamiento seguro del token

### 2. **Dashboard** (`/dashboard`)
Pantalla principal con 4 secciones:

#### 📊 **Dashboard**
- Estadísticas generales:
  - Total de alumnos
  - Total de cursos
  - Promedio general
- Información de bienvenida

#### 👥 **Alumnos**
- **Formulario de registro**: Registrar nuevos alumnos
- **Lista de alumnos**: Tabla con todos los alumnos registrados
- **Ver historial**: Modal con historial completo (cursos y notas)

#### 📚 **Cursos**
- Tabla de estadísticas de cursos:
  - Código del curso
  - Nombre
  - Créditos
  - Alumnos matriculados
  - Promedio general

#### 🧮 **Calculadora de Promedios**
- Agregar múltiples notas
- Tipo de evaluación, nota y peso
- Cálculo automático de:
  - Promedio simple
  - Promedio ponderado
  - Nota final
  - Estado (Aprobado/Desaprobado)
  - Categoría

---

## 🎨 Diseño

### Paleta de Colores:
- **Primary**: #2563eb (Azul)
- **Success**: #10b981 (Verde)
- **Danger**: #ef4444 (Rojo)
- **Warning**: #f59e0b (Amarillo)
- **Light**: #f8fafc (Gris claro)
- **Dark**: #0f172a (Negro azulado)

### Características del Diseño:
- ✅ **Responsive**: Se adapta a móviles, tablets y desktop
- ✅ **Minimalista**: Sin elementos innecesarios
- ✅ **Moderno**: Uso de sombras, bordes redondeados y transiciones
- ✅ **Accesible**: Contraste adecuado y fuentes legibles

---

## 🚀 Cómo Usar la Interfaz

### 1. Iniciar el Servidor
```bash
cd /Users/dru/Documents/Repositories/flask-alumno
source venv/bin/activate
python run.py
```

### 2. Abrir en el Navegador
```
http://localhost:5001
```

### 3. Login
- Ingresa: `admin` / `admin123`
- Click en "Iniciar Sesión"

### 4. Navegar
Usa el menú superior para cambiar entre secciones:
- 📊 Dashboard
- 👥 Alumnos
- 📚 Cursos
- 🧮 Calculadora

---

## 📋 Funcionalidades por Sección

### **Alumnos**

#### Registrar Alumno:
1. Completa el formulario con los datos del alumno
2. Click en "Registrar Alumno"
3. El alumno aparecerá en la tabla automáticamente

#### Ver Historial:
1. En la tabla de alumnos, click en "Ver Historial"
2. Se abrirá un modal con:
   - Información del alumno
   - Lista de cursos matriculados
   - Notas por curso

### **Calculadora de Promedios**

1. **Primera nota** viene por defecto
2. Click en "+ Agregar Nota" para agregar más evaluaciones
3. Completa:
   - Tipo de evaluación (ej: "Parcial 1")
   - Nota (0-20)
   - Peso en % (ej: 20 para 20%)
4. **Importante**: Los pesos deben sumar 100%
5. Click en "Calcular Promedio"
6. Se mostrará:
   - Promedio Simple
   - Promedio Ponderado
   - Nota Final (redondeada)
   - Estado: APROBADO o DESAPROBADO
   - Categoría (Desaprobado, Aprobado, Bueno, Muy Bueno, Excelente)

---

## 🔧 Arquitectura de la UI

### Estructura de Archivos:
```
app/
├── static/
│   ├── css/
│   │   └── style.css          # Estilos globales
│   └── js/
│       └── app.js             # Lógica de la aplicación
└── templates/
    ├── login.html             # Página de login
    └── dashboard.html         # Dashboard principal
```

### Tecnologías:
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos (Grid, Flexbox, Variables CSS)
- **JavaScript Vanilla**: Sin frameworks, código nativo
- **Fetch API**: Para llamadas a la API REST
- **LocalStorage**: Almacenamiento del token JWT

---

## 🔐 Seguridad

- ✅ Token JWT almacenado en LocalStorage
- ✅ Validación de sesión en cada página
- ✅ Redirección automática si no hay token
- ✅ Cierre de sesión limpia

---

## 📱 Responsive Design

La interfaz se adapta a diferentes tamaños de pantalla:

- **Desktop** (> 768px): Vista completa con grids de múltiples columnas
- **Tablet** (768px): Ajuste de columnas y espaciado
- **Mobile** (< 768px): Vista de una columna, menú scrollable

---

## 🎯 Flujo de Usuario

```
1. Login (/) 
   ↓
2. Dashboard (/dashboard)
   ↓
3. Navegar entre secciones
   ├─ Dashboard: Ver estadísticas
   ├─ Alumnos: Registrar y consultar
   ├─ Cursos: Ver estadísticas
   └─ Calculadora: Calcular promedios
   ↓
4. Cerrar Sesión
```

---

## 🐛 Solución de Problemas

### Error: "Token es requerido"
- Vuelve a hacer login
- Verifica que el servidor esté corriendo

### Error: "Failed to fetch"
- Verifica que el servidor esté en http://localhost:5001
- Revisa la consola del navegador (F12)

### No se ven los estilos
- Verifica que exista: `app/static/css/style.css`
- Limpia caché del navegador (Ctrl + F5)

### No carga JavaScript
- Verifica que exista: `app/static/js/app.js`
- Abre consola del navegador para ver errores

---

## 🎨 Personalización

### Cambiar Colores:
Edita las variables CSS en `app/static/css/style.css`:

```css
:root {
    --primary: #2563eb;      /* Azul principal */
    --success: #10b981;      /* Verde */
    --danger: #ef4444;       /* Rojo */
    /* ... más variables ... */
}
```

### Cambiar Logo:
Edita el header en `app/templates/dashboard.html`:

```html
<div class="logo">🎓 Sistema de Alumnos</div>
```

---

## 📸 Screenshots

### Login
- Formulario simple y limpio
- Credenciales de prueba visibles
- Alertas de error

### Dashboard
- Tarjetas de estadísticas
- Navegación intuitiva
- Diseño moderno

### Alumnos
- Formulario de registro claro
- Tabla responsive
- Modal de historial detallado

### Calculadora
- Agregar múltiples notas dinámicamente
- Validación de pesos (suma = 100%)
- Resultados visuales y claros

---

## 🚀 Próximas Mejoras (Opcionales)

- [ ] Paginación en tablas
- [ ] Búsqueda y filtros
- [ ] Editar/Eliminar alumnos
- [ ] Gráficos con Chart.js
- [ ] Exportar a PDF/Excel
- [ ] Notificaciones toast
- [ ] Modo oscuro
- [ ] Animaciones

---

## ✅ Checklist de Verificación

- [x] Login funcional
- [x] Dashboard con estadísticas
- [x] Registro de alumnos
- [x] Lista de alumnos
- [x] Ver historial de alumno
- [x] Estadísticas de cursos
- [x] Calculadora de promedios
- [x] Responsive design
- [x] Manejo de errores
- [x] Loading states
- [x] Cierre de sesión

---

## 🎉 ¡UI Completa!

La interfaz está lista para usar. Ahora tienes:
- ✅ **Backend API REST** completo
- ✅ **Frontend UI** minimalista y funcional
- ✅ **Base de datos** MySQL configurada
- ✅ **Documentación** completa para JMeter

**¡El sistema está 100% funcional!** 🚀
