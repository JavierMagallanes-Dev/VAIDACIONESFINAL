from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║  🚀 API Sistema de Gestión de Alumnos                   ║
    ║                                                          ║
    ║  Servidor corriendo en: http://localhost:{port}         ║
    ║  Documentación: http://localhost:{port}/                ║
    ║  Health Check: http://localhost:{port}/health           ║
    ╚══════════════════════════════════════════════════════════╝
    
    📌 Usuario de prueba:
       username: admin
       password: admin123
    
    🔗 Endpoints principales:
       POST /api/login
       POST /api/alumno/registrar
       GET  /api/historial/<id>
       GET  /api/cursos/estadisticas
       POST /api/simular-promedio
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
