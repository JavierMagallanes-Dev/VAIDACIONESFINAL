import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'tu_clave_secreta')

def generate_token(user_id, username):
    """Genera un token JWT para el usuario"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token

def token_required(f):
    """Decorador para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token es requerido'}), 401
        
        try:
            # Remover 'Bearer ' si existe
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.user_data = data
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    
    return decorated
