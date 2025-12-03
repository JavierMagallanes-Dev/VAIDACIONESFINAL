from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'tu_clave_secreta')
    app.config['JSON_SORT_KEYS'] = False
    
    # Habilitar CORS
    CORS(app)
    
    # Registrar Blueprints
    from app.routes.auth import auth_bp
    from app.routes.alumno import alumno_bp
    from app.routes.curso import curso_bp
    from app.routes.calculo import calculo_bp
    from app.routes.views import views_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(alumno_bp, url_prefix='/api')
    app.register_blueprint(curso_bp, url_prefix='/api')
    app.register_blueprint(views_bp)
    
    # Ruta de API info
    @app.route('/api')
    def index():
        return {
            'success': True,
            'message': 'API Sistema de Gestión de Alumnos',
            'version': '1.0',
            'endpoints': {
                'auth': '/api/login',
                'alumnos': {
                    'registrar': 'POST /api/alumno/registrar',
                    'listar': 'GET /api/alumnos',
                    'obtener': 'GET /api/alumno/<id>',
                    'historial': 'GET /api/historial/<id>'
                },
                'cursos': {
                    'disponibles': 'GET /api/cursos/disponibles',
                    'estadisticas': 'GET /api/cursos/estadisticas',
                    'obtener': 'GET /api/curso/<id>'
                },
                'calculos': {
                    'simular_promedio': 'POST /api/simular-promedio',
                    'simular_promedio_simple': 'POST /api/simular-promedio-simple'
                }
            }
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app
