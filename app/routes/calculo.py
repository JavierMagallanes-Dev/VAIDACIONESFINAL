from flask import Blueprint, request, jsonify
from app.utils.auth import token_required

calculo_bp = Blueprint('calculo', __name__)

@calculo_bp.route('/simular-promedio', methods=['POST'])
@token_required
def simular_promedio():
    """
    Endpoint para cálculo en memoria (CPU-intensive)
    No accede a la base de datos, solo procesa datos en memoria
    
    Ideal para probar la capacidad de procesamiento puro del servidor
    sin cuellos de botella de I/O de base de datos
    
    Body JSON:
    {
        "notas": [
            {"tipo": "Parcial 1", "nota": 15.5, "peso": 0.20},
            {"tipo": "Parcial 2", "nota": 17.0, "peso": 0.20},
            {"tipo": "Prácticas", "nota": 18.0, "peso": 0.30},
            {"tipo": "Final", "nota": 16.5, "peso": 0.30}
        ],
        "sistema": "20",
        "nota_minima_aprobacion": 10.5
    }
    
    Respuesta:
    {
        "success": true,
        "resultado": {
            "promedio_simple": 16.75,
            "promedio_ponderado": 16.85,
            "nota_final": 17,
            "aprobado": true,
            "categoria": "Bueno",
            "detalles": {...}
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('notas'):
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar una lista de notas'
            }), 400
        
        notas_list = data['notas']
        sistema = int(data.get('sistema', 20))  # Sistema vigesimal por defecto
        nota_minima = float(data.get('nota_minima_aprobacion', 10.5))
        
        # Validar que las notas sean listas con al menos un elemento
        if not isinstance(notas_list, list) or len(notas_list) == 0:
            return jsonify({
                'success': False,
                'error': 'La lista de notas debe contener al menos un elemento'
            }), 400
        
        # Validar estructura de cada nota
        suma_pesos = 0
        suma_ponderada = 0
        suma_simple = 0
        notas_validas = []
        
        for nota_obj in notas_list:
            if not isinstance(nota_obj, dict):
                return jsonify({
                    'success': False,
                    'error': 'Cada nota debe ser un objeto con tipo, nota y peso'
                }), 400
            
            tipo = nota_obj.get('tipo', 'Sin tipo')
            nota = float(nota_obj.get('nota', 0))
            peso = float(nota_obj.get('peso', 1.0))
            
            # Validar rango de nota
            if nota < 0 or nota > sistema:
                return jsonify({
                    'success': False,
                    'error': f'La nota {nota} está fuera del rango válido (0-{sistema})'
                }), 400
            
            # Validar peso
            if peso < 0 or peso > 1:
                return jsonify({
                    'success': False,
                    'error': f'El peso {peso} debe estar entre 0 y 1'
                }), 400
            
            suma_pesos += peso
            suma_ponderada += nota * peso
            suma_simple += nota
            
            notas_validas.append({
                'tipo': tipo,
                'nota': nota,
                'peso': peso,
                'contribucion': round(nota * peso, 2)
            })
        
        # Validar que los pesos sumen aproximadamente 1 (con tolerancia de 0.01)
        if abs(suma_pesos - 1.0) > 0.01:
            return jsonify({
                'success': False,
                'error': f'La suma de pesos debe ser 1.0 (actual: {suma_pesos})',
                'sugerencia': 'Ajuste los pesos para que sumen exactamente 1.0'
            }), 400
        
        # Cálculos
        cantidad_notas = len(notas_validas)
        promedio_simple = suma_simple / cantidad_notas
        promedio_ponderado = suma_ponderada / suma_pesos  # Normalizar por si los pesos no suman exactamente 1
        
        # Redondeo según sistema educativo peruano (redondeo aritmético al entero más cercano)
        nota_final = round(promedio_ponderado)
        
        # Determinar si aprobó
        aprobado = promedio_ponderado >= nota_minima
        
        # Categorizar la nota
        if sistema == 20:  # Sistema vigesimal peruano
            if promedio_ponderado < nota_minima:
                categoria = "Desaprobado"
            elif promedio_ponderado < 13:
                categoria = "Aprobado"
            elif promedio_ponderado < 16:
                categoria = "Bueno"
            elif promedio_ponderado < 18:
                categoria = "Muy Bueno"
            else:
                categoria = "Excelente"
        else:
            categoria = "Aprobado" if aprobado else "Desaprobado"
        
        # Calcular desviación estándar (para hacer el cálculo más CPU-intensive)
        varianza = sum((n['nota'] - promedio_simple) ** 2 for n in notas_validas) / cantidad_notas
        desviacion_estandar = varianza ** 0.5
        
        # Calcular nota más alta y más baja
        nota_maxima = max(n['nota'] for n in notas_validas)
        nota_minima_obtenida = min(n['nota'] for n in notas_validas)
        
        # Calcular la contribución porcentual de cada nota al promedio final
        for nota in notas_validas:
            nota['porcentaje_contribucion'] = round((nota['contribucion'] / promedio_ponderado) * 100, 2)
        
        resultado = {
            'promedio_simple': round(promedio_simple, 2),
            'promedio_ponderado': round(promedio_ponderado, 2),
            'nota_final': nota_final,
            'aprobado': aprobado,
            'categoria': categoria,
            'sistema_evaluacion': sistema,
            'nota_minima_aprobacion': nota_minima,
            'detalles': {
                'cantidad_evaluaciones': cantidad_notas,
                'nota_maxima': nota_maxima,
                'nota_minima': nota_minima_obtenida,
                'desviacion_estandar': round(desviacion_estandar, 2),
                'suma_pesos': round(suma_pesos, 2)
            },
            'notas_detalladas': notas_validas
        }
        
        return jsonify({
            'success': True,
            'resultado': resultado
        }), 200
        
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': f'Error en los datos numéricos: {str(ve)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al calcular promedio: {str(e)}'
        }), 500

@calculo_bp.route('/simular-promedio-simple', methods=['POST'])
def simular_promedio_simple():
    """
    Versión simplificada sin autenticación para pruebas rápidas
    
    Body JSON:
    {
        "notas": [15, 17, 18, 16]
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('notas'):
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar una lista de notas'
            }), 400
        
        notas = data['notas']
        
        if not isinstance(notas, list) or len(notas) == 0:
            return jsonify({
                'success': False,
                'error': 'Las notas deben ser una lista no vacía'
            }), 400
        
        # Convertir a números
        notas_numericas = [float(n) for n in notas]
        
        # Cálculos simples
        promedio = sum(notas_numericas) / len(notas_numericas)
        aprobado = promedio >= 10.5
        
        return jsonify({
            'success': True,
            'promedio': round(promedio, 2),
            'aprobado': aprobado,
            'cantidad_notas': len(notas_numericas)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500
