from app.utils.database import execute_query

class Curso:
    @staticmethod
    def crear(codigo_curso, nombre, creditos, descripcion=None):
        """Crea un nuevo curso"""
        query = """
            INSERT INTO cursos (codigo_curso, nombre, creditos, descripcion)
            VALUES (%s, %s, %s, %s)
        """
        try:
            curso_id = execute_query(query, (codigo_curso, nombre, creditos, descripcion))
            return {'success': True, 'id': curso_id}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def obtener_por_id(curso_id):
        """Obtiene un curso por su ID"""
        query = "SELECT * FROM cursos WHERE id = %s"
        return execute_query(query, (curso_id,), fetch_one=True)
    
    @staticmethod
    def obtener_disponibles():
        """Obtiene todos los cursos disponibles"""
        query = "SELECT * FROM cursos ORDER BY nombre"
        return execute_query(query, fetch=True)
    
    @staticmethod
    def obtener_con_matriculas():
        """Obtiene cursos con el conteo de alumnos matriculados (consulta pesada con JOIN)"""
        query = """
            SELECT 
                c.id,
                c.codigo_curso,
                c.nombre,
                c.creditos,
                c.descripcion,
                COUNT(DISTINCT m.alumno_id) as total_alumnos,
                COUNT(DISTINCT n.id) as total_evaluaciones,
                AVG(n.nota) as promedio_general
            FROM cursos c
            LEFT JOIN matriculas m ON c.id = m.curso_id
            LEFT JOIN notas n ON m.id = n.matricula_id
            GROUP BY c.id, c.codigo_curso, c.nombre, c.creditos, c.descripcion
            ORDER BY c.nombre
        """
        return execute_query(query, fetch=True)
