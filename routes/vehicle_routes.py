from flask import Blueprint, request, jsonify
from services.vehicle_service import VehicleService

vehicle_bp = Blueprint('vehicle', __name__)
vehicle_service = VehicleService()

# --- Commission Routes ---
@vehicle_bp.route('/list', methods=['GET'])
def get_requests():
    requests = vehicle_service.get_all_requests()
    return jsonify(requests)

@vehicle_bp.route('/create', methods=['POST'])
def create_request():
    data = request.get_json()
    try:
        req_id = vehicle_service.create_request(data)
        return jsonify({'id': req_id, 'message': 'Solicitud creada correctamente'}), 201
    except Exception as e:
        return jsonify({'message': f'Error al crear solicitud: {str(e)}'}), 500

@vehicle_bp.route('/update/<id>', methods=['PUT'])
def update_request(id):
    data = request.get_json()
    try:
        success = vehicle_service.update_request(id, data)
        if success:
            return jsonify({'message': 'Solicitud actualizada correctamente'}), 200
        return jsonify({'message': 'Solicitud no encontrada'}), 404
    except Exception as e:
        return jsonify({'message': f'Error al actualizar solicitud: {str(e)}'}), 500

# --- Inventory Routes ---
@vehicle_bp.route('/inventory/list', methods=['GET'])
def get_vehicles():
    vehicles = vehicle_service.get_all_vehicles()
    return jsonify(vehicles)

@vehicle_bp.route('/inventory/create', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    try:
        veh_id = vehicle_service.create_vehicle(data)
        return jsonify({'id': veh_id, 'message': 'Vehículo registrado correctamente'}), 201
    except Exception as e:
        return jsonify({'message': f'Error al registrar vehículo: {str(e)}'}), 500

@vehicle_bp.route('/inventory/update/<id>', methods=['PUT'])
def update_vehicle(id):
    data = request.get_json()
    try:
        success = vehicle_service.update_vehicle(id, data)
        if success:
            return jsonify({'message': 'Vehículo actualizado correctamente'}), 200
        return jsonify({'message': 'Vehículo no encontrado'}), 404
    except Exception as e:
        return jsonify({'message': f'Error al actualizar vehículo: {str(e)}'}), 500

# --- Maintenance Routes ---
@vehicle_bp.route('/maintenance/list', methods=['GET'])
def get_maintenance_expenses():
    expenses = vehicle_service.get_all_maintenance_expenses()
    return jsonify(expenses)

@vehicle_bp.route('/maintenance/create', methods=['POST'])
def create_maintenance_expense():
    data = request.get_json()
    try:
        expense_id = vehicle_service.create_maintenance_expense(data)
        return jsonify({'id': expense_id, 'message': 'Gasto de mantenimiento registrado correctamente'}), 201
    except Exception as e:
        return jsonify({'message': f'Error al registrar gasto de mantenimiento: {str(e)}'}), 500

# --- Handover Routes ---
@vehicle_bp.route('/handover/list', methods=['GET'])
def get_handovers():
    handovers = vehicle_service.get_all_handovers()
    return jsonify(handovers)

@vehicle_bp.route('/handover/create', methods=['POST'])
def create_handover():
    data = request.get_json()
    try:
        handover_id = vehicle_service.create_handover(data)
        return jsonify({'id': handover_id, 'message': 'Acta de entrega registrada correctamente'}), 201
    except Exception as e:
        return jsonify({'message': f'Error al registrar acta: {str(e)}'}), 500

# --- Service Requirements Routes ---
@vehicle_bp.route('/service-requirements/list', methods=['GET'])
def get_service_requirements():
    reqs = vehicle_service.get_all_service_requirements()
    return jsonify(reqs)

@vehicle_bp.route('/service-requirements/create', methods=['POST'])
def create_service_requirement():
    data = request.get_json()
    try:
        req_id = vehicle_service.create_service_requirement(data)
        return jsonify({'id': req_id, 'message': 'Requerimiento registrado correctamente'}), 201
    except Exception as e:
        return jsonify({'message': f'Error al registrar requerimiento: {str(e)}'}), 500
