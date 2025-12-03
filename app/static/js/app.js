// API Configuration
const API_BASE_URL = 'http://localhost:5001/api';
let authToken = localStorage.getItem('token');

// API Helper
async function apiCall(endpoint, method = 'GET', data = null) {
    const headers = {
        'Content-Type': 'application/json',
    };

    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }

    const config = {
        method,
        headers,
    };

    if (data && method !== 'GET') {
        config.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Error en la petición');
        }

        return result;
    } catch (error) {
        throw error;
    }
}

// Alert Helper
function showAlert(message, type = 'success') {
    const alertDiv = document.getElementById('alert');
    alertDiv.className = `alert alert-${type} show`;
    alertDiv.textContent = message;

    setTimeout(() => {
        alertDiv.classList.remove('show');
    }, 5000);
}

// Loading Helper
function showLoading(show = true) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.add('show');
    } else {
        loading.classList.remove('show');
    }
}

// Navigation
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.section');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const target = item.dataset.section;

            // Update active nav item
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Show target section
            sections.forEach(section => section.classList.remove('active'));
            document.getElementById(`${target}-section`).classList.add('active');

            // Load section data
            loadSectionData(target);
        });
    });
}

// Load Section Data
async function loadSectionData(section) {
    switch (section) {
        case 'dashboard':
            await loadDashboard();
            break;
        case 'alumnos':
            await loadAlumnos();
            break;
        case 'cursos':
            await loadCursos();
            break;
        case 'calculadora':
            // No need to load data
            break;
    }
}

// Dashboard
async function loadDashboard() {
    try {
        showLoading(true);

        // Load statistics
        const [alumnos, cursos] = await Promise.all([
            apiCall('/alumnos?limit=1000'),
            apiCall('/cursos/estadisticas')
        ]);

        document.getElementById('total-alumnos').textContent = alumnos.count || 0;
        document.getElementById('total-cursos').textContent = cursos.total_cursos || 0;

        // Calculate average
        let totalPromedio = 0;
        let count = 0;
        cursos.cursos.forEach(curso => {
            if (curso.estadisticas.promedio_general > 0) {
                totalPromedio += curso.estadisticas.promedio_general;
                count++;
            }
        });
        const promedioGeneral = count > 0 ? (totalPromedio / count).toFixed(2) : 0;
        document.getElementById('promedio-general').textContent = promedioGeneral;

        showLoading(false);
    } catch (error) {
        showLoading(false);
        showAlert(error.message, 'error');
    }
}

// Alumnos
async function loadAlumnos() {
    try {
        showLoading(true);
        const data = await apiCall('/alumnos?limit=100');
        
        const tbody = document.getElementById('alumnos-tbody');
        tbody.innerHTML = '';

        data.alumnos.forEach(alumno => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${alumno.codigo}</td>
                <td>${alumno.nombre} ${alumno.apellido}</td>
                <td>${alumno.dni}</td>
                <td>${alumno.email || '-'}</td>
                <td>${alumno.telefono || '-'}</td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="verHistorial(${alumno.id})">
                        Ver Historial
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        showLoading(false);
    } catch (error) {
        showLoading(false);
        showAlert(error.message, 'error');
    }
}

// Register Alumno
async function registrarAlumno(event) {
    event.preventDefault();

    const formData = {
        codigo: document.getElementById('codigo').value,
        dni: document.getElementById('dni').value,
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        email: document.getElementById('email').value,
        telefono: document.getElementById('telefono').value,
        fecha_ingreso: document.getElementById('fecha_ingreso').value
    };

    try {
        showLoading(true);
        await apiCall('/alumno/registrar', 'POST', formData);
        showAlert('Alumno registrado exitosamente');
        document.getElementById('alumno-form').reset();
        await loadAlumnos();
        showLoading(false);
    } catch (error) {
        showLoading(false);
        showAlert(error.message, 'error');
    }
}

// Ver Historial
async function verHistorial(alumnoId) {
    try {
        showLoading(true);
        const data = await apiCall(`/historial/${alumnoId}`);
        
        let html = `
            <div class="card">
                <div class="card-header">
                    <h3>Historial de ${data.alumno.nombre} ${data.alumno.apellido}</h3>
                    <button class="btn btn-secondary" onclick="closeModal()">Cerrar</button>
                </div>
                <p><strong>Código:</strong> ${data.alumno.codigo} | <strong>DNI:</strong> ${data.alumno.dni}</p>
        `;

        if (data.historial.length > 0) {
            data.historial.forEach(curso => {
                html += `
                    <div class="card" style="margin-top: 1rem; background: var(--light);">
                        <h4>${curso.nombre} (${curso.codigo_curso})</h4>
                        <p><strong>Semestre:</strong> ${curso.semestre} ${curso.anio} | <strong>Créditos:</strong> ${curso.creditos}</p>
                `;

                if (curso.notas.length > 0) {
                    html += '<table><thead><tr><th>Evaluación</th><th>Nota</th><th>Peso</th></tr></thead><tbody>';
                    curso.notas.forEach(nota => {
                        html += `
                            <tr>
                                <td>${nota.tipo_evaluacion}</td>
                                <td>${nota.nota}</td>
                                <td>${(nota.peso * 100).toFixed(0)}%</td>
                            </tr>
                        `;
                    });
                    html += '</tbody></table>';
                } else {
                    html += '<p>Sin notas registradas</p>';
                }

                html += '</div>';
            });
        } else {
            html += '<p>No hay cursos registrados para este alumno.</p>';
        }

        html += '</div>';

        // Show modal
        const modal = document.createElement('div');
        modal.id = 'modal';
        modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 2rem; overflow-y: auto;';
        modal.innerHTML = `<div style="max-width: 800px; width: 100%; max-height: 90vh; overflow-y: auto;">${html}</div>`;
        document.body.appendChild(modal);

        showLoading(false);
    } catch (error) {
        showLoading(false);
        showAlert(error.message, 'error');
    }
}

function closeModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        modal.remove();
    }
}

// Cursos
async function loadCursos() {
    try {
        showLoading(true);
        const data = await apiCall('/cursos/estadisticas');
        
        const tbody = document.getElementById('cursos-tbody');
        tbody.innerHTML = '';

        data.cursos.forEach(curso => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${curso.codigo}</td>
                <td>${curso.nombre}</td>
                <td>${curso.creditos}</td>
                <td>${curso.estadisticas.total_alumnos_matriculados}</td>
                <td>${curso.estadisticas.promedio_general}</td>
            `;
            tbody.appendChild(tr);
        });

        showLoading(false);
    } catch (error) {
        showLoading(false);
        showAlert(error.message, 'error');
    }
}

// Calculadora
function agregarNota() {
    const notasContainer = document.getElementById('notas-container');
    const index = notasContainer.children.length + 1;
    
    const notaDiv = document.createElement('div');
    notaDiv.className = 'form-row';
    notaDiv.style.marginBottom = '1rem';
    notaDiv.innerHTML = `
        <div class="form-group">
            <label class="form-label">Tipo Evaluación ${index}</label>
            <input type="text" class="form-input nota-tipo" placeholder="Ej: Parcial 1" required>
        </div>
        <div class="form-group">
            <label class="form-label">Nota</label>
            <input type="number" class="form-input nota-valor" min="0" max="20" step="0.5" required>
        </div>
        <div class="form-group">
            <label class="form-label">Peso (%)</label>
            <input type="number" class="form-input nota-peso" min="0" max="100" step="1" required>
        </div>
    `;
    
    notasContainer.appendChild(notaDiv);
}

async function calcularPromedio(event) {
    event.preventDefault();

    const tipos = document.querySelectorAll('.nota-tipo');
    const valores = document.querySelectorAll('.nota-valor');
    const pesos = document.querySelectorAll('.nota-peso');

    const notas = [];
    let totalPeso = 0;

    for (let i = 0; i < tipos.length; i++) {
        const peso = parseFloat(pesos[i].value) / 100;
        totalPeso += parseFloat(pesos[i].value);
        
        notas.push({
            tipo: tipos[i].value,
            nota: parseFloat(valores[i].value),
            peso: peso
        });
    }

    if (Math.abs(totalPeso - 100) > 0.1) {
        showAlert('La suma de los pesos debe ser 100%', 'error');
        return;
    }

    const data = {
        notas: notas,
        sistema: 20,
        nota_minima_aprobacion: 10.5
    };

    try {
        showLoading(true);
        const result = await apiCall('/simular-promedio', 'POST', data);
        
        const resultadoDiv = document.getElementById('resultado-calculo');
        resultadoDiv.innerHTML = `
            <div class="card">
                <h3>Resultado del Cálculo</h3>
                <div class="stats-grid" style="margin-top: 1rem;">
                    <div class="stat-card">
                        <div class="stat-label">Promedio Simple</div>
                        <div class="stat-value">${result.resultado.promedio_simple}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Promedio Ponderado</div>
                        <div class="stat-value">${result.resultado.promedio_ponderado}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Nota Final</div>
                        <div class="stat-value">${result.resultado.nota_final}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Estado</div>
                        <div class="stat-value" style="color: ${result.resultado.aprobado ? 'var(--success)' : 'var(--danger)'}">
                            ${result.resultado.aprobado ? 'APROBADO' : 'DESAPROBADO'}
                        </div>
                    </div>
                </div>
                <p style="margin-top: 1rem;"><strong>Categoría:</strong> ${result.resultado.categoria}</p>
            </div>
        `;

        showLoading(false);
    } catch (error) {
        showLoading(false);
        showAlert(error.message, 'error');
    }
}

// Logout
function logout() {
    localStorage.removeItem('token');
    window.location.reload();
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadDashboard();
});
