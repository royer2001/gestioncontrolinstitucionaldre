from flask import Blueprint, request, jsonify
from services.turn_service import TurnService

turn_bp = Blueprint('turn', __name__)
turn_service = TurnService()  # Se inicializa pero no conecta a Google


@turn_bp.route('/areas', methods=['GET'])
def get_areas():
    """Obtener todas las áreas disponibles para turnos"""
    try:
        areas = turn_service.get_areas()
        return jsonify({'success': True, 'areas': areas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@turn_bp.route('/create', methods=['POST'])
def create_turn():
    """Crear un nuevo turno"""
    try:
        data = request.json
        
        if not data.get('codigo_area'):
            return jsonify({'success': False, 'error': 'Debe seleccionar un área'}), 400
        
        # Determinar quién crea el turno
        created_by = data.get('created_by', 'TOTEM')
        
        turn, error = turn_service.create_turn(data, created_by)
        
        if error:
            return jsonify({'success': False, 'error': error}), 400
        
        return jsonify({
            'success': True,
            'turno': turn,
            'message': f"Turno {turn['numero_turno']} generado exitosamente"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@turn_bp.route('/waiting', methods=['GET'])
def get_waiting_turns():
    """Obtener turnos en espera del día actual"""
    try:
        codigo_area = request.args.get('area')
        turns = turn_service.get_waiting_turns_today(codigo_area)
        return jsonify({'success': True, 'turnos': turns})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@turn_bp.route('/current', methods=['GET'])
def get_current_turns():
    """Obtener turnos que están siendo llamados actualmente"""
    try:
        turns = turn_service.get_current_turns()
        return jsonify({'success': True, 'turnos': turns})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@turn_bp.route('/display', methods=['GET'])
def get_display_data():
    """Obtener datos para la pantalla de sala de espera"""
    try:
        current_turns = turn_service.get_current_turns()
        waiting_turns = turn_service.get_waiting_turns_today()
        areas = turn_service.get_areas()
        
        # Agrupar turnos en espera por área
        waiting_by_area = {}
        for area in areas:
            codigo = area['codigo']
            area_turns = [t for t in waiting_turns if t.get('codigo_area') == codigo]
            waiting_by_area[codigo] = {
                'nombre': area['nombre'],
                'prefijo': area['prefijo'],
                'count': len(area_turns),
                'turns': area_turns[:5]  # Solo los primeros 5
            }
        
        return jsonify({
            'success': True,
            'current': current_turns,
            'waiting_by_area': waiting_by_area,
            'total_waiting': len(waiting_turns)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@turn_bp.route('/call-next', methods=['POST'])
def call_next_turn():
    """Llamar al siguiente turno de un área"""
    try:
        data = request.json
        codigo_area = data.get('codigo_area')
        ventanilla = data.get('ventanilla', '1')
        user = data.get('user', 'Sistema')
        
        if not codigo_area:
            return jsonify({'success': False, 'error': 'Debe especificar el área'}), 400
        
        turn, error = turn_service.call_next_turn(codigo_area, ventanilla, user)
        
        if error:
            return jsonify({'success': False, 'error': error}), 400
        
        return jsonify({
            'success': True,
            'turno': turn,
            'message': f"Llamando turno {turn['numero_turno']}"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@turn_bp.route('/complete/<turn_id>', methods=['POST'])
def complete_turn(turn_id):
    """Marcar un turno como atendido"""
    try:
        data = request.json or {}
        user = data.get('user', 'Sistema')
        
        success, error = turn_service.complete_turn(turn_id, user)
        
        if error:
            return jsonify({'success': False, 'error': error}), 400
        
        return jsonify({'success': True, 'message': 'Turno completado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@turn_bp.route('/cancel/<turn_id>', methods=['POST'])
def cancel_turn(turn_id):
    """Cancelar un turno (no se presentó)"""
    try:
        data = request.json or {}
        user = data.get('user', 'Sistema')
        
        success, error = turn_service.cancel_turn(turn_id, user)
        
        if error:
            return jsonify({'success': False, 'error': error}), 400
        
        return jsonify({'success': True, 'message': 'Turno cancelado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@turn_bp.route('/by-date', methods=['GET'])
def get_turns_by_date():
    """Obtener turnos por fecha"""
    try:
        fecha = request.args.get('fecha')
        turns = turn_service.get_turns_by_date(fecha)
        return jsonify({'success': True, 'turnos': turns})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@turn_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Obtener estadísticas de turnos"""
    try:
        fecha = request.args.get('fecha')
        stats = turn_service.get_statistics(fecha)
        return jsonify({'success': True, 'estadisticas': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
