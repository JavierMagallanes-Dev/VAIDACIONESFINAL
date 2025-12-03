import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Crea y devuelve una conexión a la base de datos MySQL"""
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'root'),
        database=os.getenv('DB_NAME', 'sistema_alumnos'),
        port=int(os.getenv('DB_PORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
    return connection

def execute_query(query, params=None, fetch=False, fetch_one=False):
    """
    Ejecuta una consulta SQL
    
    Args:
        query: Consulta SQL a ejecutar
        params: Parámetros para la consulta
        fetch: Si True, devuelve todos los resultados
        fetch_one: Si True, devuelve solo un resultado
    
    Returns:
        Resultados de la consulta o None
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch:
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid
            
            connection.commit()
            return result
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
