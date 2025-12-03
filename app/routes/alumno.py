from flask import Blueprint, request, jsonify
from app.models.alumno import Alumno
from app.utils.auth import token_required
from datetime import datetime

alumno_bp = Blueprint('alumno', __name__)

@alumno_bp.route('/alumno/registrar', methods=['POST'])
@token_required
def registrar_alumno():
    """
    Endpoint para registrar un alumno
    Ideal para pruebas de escritura masiva en JMeter con CSV Data Set Config
    
    Body JSON:
    {
        "codigo": "A001",
        "dni": "12345678",
        "nombre": "Juan",
        "apellido": "Pérez",
        "email": "juan@email.com",
        "telefono": "987654321",
        "fecha_ingreso": "2024-01-15"
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        campos_requeridos = ['codigo', 'dni', 'nombre', 'apellido']
        for campo in campos_requeridos:
            if not data.get(campo):
                return jsonify({
                    'success': False,
                    'error': f'El campo {campo} es requerido'
                }), 400
        
        # Validar DNI (8 dígitos)
        if not data['dni'].isdigit() or len(data['dni']) != 8:
            return jsonify({
                'success': False,
                'error': 'DNI debe tener 8 dígitos numéricos'
            }), 400
        
        # Crear el alumno
        resultado = Alumno.crear(
            codigo=data['codigo'],
            dni=data['dni'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data.get('email'),
            telefono=data.get('telefono'),
            fecha_ingreso=data.get('fecha_ingreso')
        )
        
        if resultado['success']:
            return jsonify({
                'success': True,
                'message': 'Alumno registrado exitosamente',
                'alumno_id': resultado['id']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': resultado['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al registrar alumno: {str(e)}'
        }), 500

@alumno_bp.route('/alumno/<int:alumno_id>', methods=['GET'])
@token_required
def obtener_alumno(alumno_id):
    """Obtiene los datos de un alumno por ID"""
    try:
        alumno = Alumno.obtener_por_id(alumno_id)
        
        if not alumno:
            return jsonify({
                'success': False,
                'error': 'Alumno no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'alumno': alumno
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener alumno: {str(e)}'
        }), 500

@alumno_bp.route('/alumnos', methods=['GET'])
@token_required
def listar_alumnos():
    """Lista todos los alumnos con paginación"""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        alumnos = Alumno.obtener_todos(limit=limit, offset=offset)
        
        return jsonify({
            'success': True,
            'alumnos': alumnos,
            'count': len(alumnos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al listar alumnos: {str(e)}'
        }), 500

@alumno_bp.route('/historial/<int:alumno_id>', methods=['GET'])
@token_required
def obtener_historial(alumno_id):
    """
    Obtiene el historial completo de un alumno
    Consulta pesada con múltiples JOINs (Alumnos + Cursos + Matrículas + Notas)
    Ideal para pruebas de lectura intensiva en JMeter
    """
    try:
        historial = Alumno.obtener_historial_completo(alumno_id)
        
        if not historial:
            return jsonify({
                'success': False,
                'error': 'No se encontró historial para este alumno'
            }), 404
        
        # Organizar los datos
        alumno_info = {
            'alumno_id': historial[0]['alumno_id'],
            'codigo': historial[0]['alumno_codigo'],
            'nombre': historial[0]['nombre'],
            'apellido': historial[0]['apellido'],
            'dni': historial[0]['dni']
        }
        
        cursos = {}
        for registro in historial:
            if registro['curso_id']:
                curso_key = f"{registro['curso_id']}_{registro['semestre']}_{registro['anio']}"
                
                if curso_key not in cursos:
                    cursos[curso_key] = {
                        'curso_id': registro['curso_id'],
                        'codigo_curso': registro['codigo_curso'],
                        'nombre': registro['curso_nombre'],
                        'creditos': registro['creditos'],
                        'semestre': registro['semestre'],
                        'anio': registro['anio'],
                        'fecha_matricula': str(registro['fecha_matricula']) if registro['fecha_matricula'] else None,
                        'notas': []
                    }
                
                if registro['nota'] is not None:
                    cursos[curso_key]['notas'].append({
                        'tipo_evaluacion': registro['tipo_evaluacion'],
                        'nota': float(registro['nota']),
                        'peso': float(registro['peso']),
                        'fecha_evaluacion': str(registro['fecha_evaluacion']) if registro['fecha_evaluacion'] else None
                    })
        
        return jsonify({
            'success': True,
            'alumno': alumno_info,
            'historial': list(cursos.values()),
            'total_cursos': len(cursos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener historial: {str(e)}'
        }), 500
