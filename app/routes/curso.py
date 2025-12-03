from flask import Blueprint, request, jsonify
from app.models.curso import Curso
from app.utils.auth import token_required

curso_bp = Blueprint('curso', __name__)

@curso_bp.route('/cursos/disponibles', methods=['GET'])
@token_required
def listar_cursos_disponibles():
    """
    Lista todos los cursos disponibles
    Consulta simple para comparar con la consulta pesada
    """
    try:
        cursos = Curso.obtener_disponibles()
        
        return jsonify({
            'success': True,
            'cursos': cursos,
            'total': len(cursos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener cursos: {str(e)}'
        }), 500

@curso_bp.route('/cursos/estadisticas', methods=['GET'])
@token_required
def obtener_estadisticas_cursos():
    """
    Obtiene estadísticas de cursos con múltiples JOINs
    Consulta PESADA que une: Cursos + Matrículas + Notas
    Ideal para pruebas de latencia y tiempo de respuesta en JMeter
    
    Esta consulta:
    - Une 3 tablas con LEFT JOINs
    - Calcula agregaciones (COUNT, AVG)
    - Agrupa por varios campos
    - Simula una consulta real de reportes
    """
    try:
        estadisticas = Curso.obtener_con_matriculas()
        
        # Procesar estadísticas para formato más legible
        resultado = []
        for curso in estadisticas:
            resultado.append({
                'curso_id': curso['id'],
                'codigo': curso['codigo_curso'],
                'nombre': curso['nombre'],
                'creditos': curso['creditos'],
                'descripcion': curso['descripcion'],
                'estadisticas': {
                    'total_alumnos_matriculados': curso['total_alumnos'],
                    'total_evaluaciones_realizadas': curso['total_evaluaciones'],
                    'promedio_general': round(float(curso['promedio_general']), 2) if curso['promedio_general'] else 0
                }
            })
        
        return jsonify({
            'success': True,
            'cursos': resultado,
            'total_cursos': len(resultado)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener estadísticas: {str(e)}'
        }), 500

@curso_bp.route('/curso/<int:curso_id>', methods=['GET'])
@token_required
def obtener_curso(curso_id):
    """Obtiene información de un curso específico"""
    try:
        curso = Curso.obtener_por_id(curso_id)
        
        if not curso:
            return jsonify({
                'success': False,
                'error': 'Curso no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'curso': curso
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener curso: {str(e)}'
        }), 500
