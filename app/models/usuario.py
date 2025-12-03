from app.utils.database import execute_query

class Usuario:
    @staticmethod
    def crear(username, password_hash, email=None):
        """Crea un nuevo usuario"""
        query = """
            INSERT INTO usuarios (username, password_hash, email)
            VALUES (%s, %s, %s)
        """
        try:
            user_id = execute_query(query, (username, password_hash, email))
            return {'success': True, 'id': user_id}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def obtener_por_username(username):
        """Obtiene un usuario por su username"""
        query = "SELECT * FROM usuarios WHERE username = %s"
        return execute_query(query, (username,), fetch_one=True)
    
    @staticmethod
    def verificar_credenciales(username, password_hash):
        """Verifica las credenciales de un usuario"""
        query = "SELECT * FROM usuarios WHERE username = %s AND password_hash = %s"
        return execute_query(query, (username, password_hash), fetch_one=True)
