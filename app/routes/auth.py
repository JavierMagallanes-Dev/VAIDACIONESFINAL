from flask import Blueprint, request, jsonify
import hashlib
from app.models.usuario import Usuario
from app.utils.auth import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint de autenticación
    
    Body JSON:
    {
        "username": "admin",
        "password": "admin123"
    }
    
    Respuesta exitosa:
    {
        "success": true,
        "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "user": {
            "id": 1,
            "username": "admin"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Username y password son requeridos'
            }), 400
        
        username = data['username']
        password = data['password']
        
        # Hash de la contraseña usando SHA256 (para CPU-intensive testing en JMeter)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Verificar credenciales
        user = Usuario.verificar_credenciales(username, password_hash)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Credenciales inválidas'
            }), 401
        
        # Generar token JWT
        token = generate_token(user['id'], user['username'])
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user.get('email')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error en autenticación: {str(e)}'
        }), 500
