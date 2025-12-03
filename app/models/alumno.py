from app.utils.database import execute_query

class Alumno:
    @staticmethod
    def crear(codigo, dni, nombre, apellido, email=None, telefono=None, fecha_ingreso=None):
        """Crea un nuevo alumno en la base de datos"""
        query = """
            INSERT INTO alumnos (codigo, dni, nombre, apellido, email, telefono, fecha_ingreso)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            alumno_id = execute_query(query, (codigo, dni, nombre, apellido, email, telefono, fecha_ingreso))
            return {'success': True, 'id': alumno_id}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def obtener_por_id(alumno_id):
        """Obtiene un alumno por su ID"""
        query = "SELECT * FROM alumnos WHERE id = %s"
        return execute_query(query, (alumno_id,), fetch_one=True)
    
    @staticmethod
    def obtener_por_dni(dni):
        """Obtiene un alumno por su DNI"""
        query = "SELECT * FROM alumnos WHERE dni = %s"
        return execute_query(query, (dni,), fetch_one=True)
    
    @staticmethod
    def obtener_todos(limit=100, offset=0):
        """Obtiene todos los alumnos con paginación"""
        query = "SELECT * FROM alumnos ORDER BY apellido, nombre LIMIT %s OFFSET %s"
        return execute_query(query, (limit, offset), fetch=True)
    
    @staticmethod
    def actualizar(alumno_id, **kwargs):
        """Actualiza los datos de un alumno"""
        campos = []
        valores = []
        
        for key, value in kwargs.items():
            if value is not None:
                campos.append(f"{key} = %s")
                valores.append(value)
        
        if not campos:
            return {'success': False, 'error': 'No hay campos para actualizar'}
        
        valores.append(alumno_id)
        query = f"UPDATE alumnos SET {', '.join(campos)} WHERE id = %s"
        
        try:
            execute_query(query, tuple(valores))
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def eliminar(alumno_id):
        """Elimina un alumno"""
        query = "DELETE FROM alumnos WHERE id = %s"
        try:
            execute_query(query, (alumno_id,))
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def obtener_historial_completo(alumno_id):
        """Obtiene el historial completo de un alumno con todos sus cursos y notas"""
        query = """
            SELECT 
                a.id as alumno_id,
                a.codigo as alumno_codigo,
                a.nombre,
                a.apellido,
                a.dni,
                c.id as curso_id,
                c.codigo_curso,
                c.nombre as curso_nombre,
                c.creditos,
                m.semestre,
                m.anio,
                m.fecha_matricula,
                n.tipo_evaluacion,
                n.nota,
                n.peso,
                n.fecha_evaluacion
            FROM alumnos a
            LEFT JOIN matriculas m ON a.id = m.alumno_id
            LEFT JOIN cursos c ON m.curso_id = c.id
            LEFT JOIN notas n ON m.id = n.matricula_id
            WHERE a.id = %s
            ORDER BY m.anio DESC, m.semestre DESC, c.nombre, n.fecha_evaluacion
        """
        return execute_query(query, (alumno_id,), fetch=True)
