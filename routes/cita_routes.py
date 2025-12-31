from flask import Blueprint, request, jsonify
from services.cita_service import CitaService

cita_bp = Blueprint('cita', __name__)
cita_service = CitaService()

@cita_bp.route('/request', methods=['POST'])
def create_cita():
    """Public endpoint - create new appointment"""
    data = request.json
    try:
        cita_id = cita_service.create_cita(data)
        return jsonify({'message': 'Cita registrada con éxito', 'id': cita_id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@cita_bp.route('/', methods=['GET'])
def get_citas():
    """Get all appointments"""
    citas = cita_service.get_all_citas()
    return jsonify(citas)

@cita_bp.route('/status/<string:dni>', methods=['GET'])
def check_status(dni):
    """Public endpoint to check status by DNI"""
    citas = cita_service.get_citas_by_dni(dni)
    return jsonify(citas)

@cita_bp.route('/<string:id>/status', methods=['PUT'])
def update_status(id):
    """Update appointment status"""
    data = request.json
    new_status = data.get('status')
    observacion = data.get('observacion') # Added this
    if not new_status:
        return jsonify({'message': 'Status is required'}), 400
    
    success = cita_service.update_cita_status(id, new_status, observacion)
    if success:
        return jsonify({'message': 'Estado actualizado correctamente'})
    else:
        return jsonify({'message': 'Error al actualizar estado'}), 500
