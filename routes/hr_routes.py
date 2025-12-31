from flask import Blueprint, request, jsonify
from services.hr_service import HRService

hr_bp = Blueprint('hr', __name__)
hr_service = HRService()

# ============ EMPLOYEE ROUTES ============

@hr_bp.route('/employees', methods=['GET'])
def get_employees():
    """Get all employees"""
    employees = hr_service.get_all_employees()
    return jsonify(employees)

@hr_bp.route('/employee', methods=['POST'])
def create_employee():
    """Create a new employee"""
    data = request.json
    
    required_fields = ['dni', 'nombres', 'apellidos']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'Campo requerido: {field}'}), 400
    
    # Check if DNI already exists
    existing = hr_service.get_employee_by_dni(data.get('dni'))
    if existing:
        return jsonify({'message': 'Ya existe un empleado con ese DNI'}), 400
    
    employee_id = hr_service.create_employee(data)
    return jsonify({
        'message': 'Empleado registrado correctamente',
        'id': employee_id
    }), 201

@hr_bp.route('/employee/<string:id>', methods=['GET'])
def get_employee(id):
    """Get employee by ID"""
    employee = hr_service.get_employee_by_id(id)
    if not employee:
        return jsonify({'message': 'Empleado no encontrado'}), 404
    
    # Get vacations and activities
    vacations = hr_service.get_vacations_by_employee(id)
    employee['vacaciones'] = vacations
    
    return jsonify(employee)

@hr_bp.route('/employee/<string:id>', methods=['PUT'])
def update_employee(id):
    """Update employee data"""
    data = request.json
    success = hr_service.update_employee(id, data)
    
    if success:
        return jsonify({'message': 'Empleado actualizado correctamente'})
    else:
        return jsonify({'message': 'Error al actualizar empleado'}), 500

@hr_bp.route('/employee/dni/<string:dni>', methods=['GET'])
def get_employee_by_dni(dni):
    """Get employee by DNI"""
    employee = hr_service.get_employee_by_dni(dni)
    if not employee:
        return jsonify({'message': 'Empleado no encontrado'}), 404
    return jsonify(employee)

# ============ VACATION ROUTES ============

@hr_bp.route('/vacations', methods=['GET'])
def get_vacations():
    """Get all vacations"""
    vacations = hr_service.get_all_vacations()
    return jsonify(vacations)

@hr_bp.route('/vacation', methods=['POST'])
def create_vacation():
    """Register a new vacation"""
    data = request.json
    
    required_fields = ['empleado_id', 'fecha_inicio', 'fecha_fin']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'Campo requerido: {field}'}), 400
    
    vacation_id = hr_service.create_vacation(data)
    return jsonify({
        'message': 'Vacaciones registradas correctamente',
        'id': vacation_id
    }), 201

# ============ ACTIVITY ROUTES ============

@hr_bp.route('/activities', methods=['GET'])
def get_activities():
    """Get all HR activities"""
    activities = hr_service.get_all_activities()
    return jsonify(activities)

@hr_bp.route('/activity', methods=['POST'])
def create_activity():
    """Register a new HR activity"""
    data = request.json
    
    required_fields = ['empleado_id', 'tipo_actividad', 'descripcion']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'Campo requerido: {field}'}), 400
    
    created_by = 'Sistema'
    if hasattr(request, 'user') and request.user:
        created_by = request.user.get('nombre', 'Sistema')
    
    activity_id = hr_service.create_activity(data, created_by)
    return jsonify({
        'message': 'Actividad registrada correctamente',
        'id': activity_id
    }), 201

# ============ SUMMARY ============

@hr_bp.route('/summary', methods=['GET'])
def get_summary():
    """Get HR summary statistics"""
    summary = hr_service.get_summary()
    return jsonify(summary)
