from flask import Blueprint, request, jsonify
from services.license_service import LicenseService

license_bp = Blueprint('license', __name__)
license_service = LicenseService()

@license_bp.route('/employees', methods=['GET'])
def get_employees():
    """Get all employees with their license balance"""
    employees = license_service.get_all_employees()
    return jsonify(employees)

@license_bp.route('/employee/<string:dni>', methods=['GET'])
def get_employee(dni):
    """Get employee by DNI with license history"""
    employee = license_service.get_employee_by_dni(dni)
    if not employee:
        return jsonify({'message': 'Empleado no encontrado'}), 404
    
    licenses = license_service.get_licenses_by_dni(dni)
    employee['licencias'] = licenses
    employee['dias_disponibles'] = int(employee.get('dias_totales', 20)) - int(employee.get('dias_usados', 0))
    
    return jsonify(employee)

@license_bp.route('/list', methods=['GET'])
def get_licenses():
    """Get all licenses"""
    licenses = license_service.get_all_licenses()
    return jsonify(licenses)

@license_bp.route('/register', methods=['POST'])
def register_license():
    """Register a new license"""
    data = request.json
    
    required_fields = ['dni', 'nombres', 'apellidos', 'tipo_licencia', 'fecha_inicio', 'fecha_fin']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'Campo requerido: {field}'}), 400
    
    created_by = 'Sistema'
    if hasattr(request, 'user') and request.user:
        created_by = request.user.get('nombre', 'Sistema')
    
    license_id, error = license_service.create_license(data, created_by)
    
    if error:
        return jsonify({'message': error}), 400
    
    return jsonify({
        'message': 'Licencia registrada correctamente',
        'id': license_id
    }), 201

@license_bp.route('/summary', methods=['GET'])
def get_summary():
    """Get license summary statistics"""
    summary = license_service.get_license_summary()
    return jsonify(summary)

@license_bp.route('/by-dni/<string:dni>', methods=['GET'])
def get_licenses_by_dni(dni):
    """Get all licenses for a specific DNI"""
    licenses = license_service.get_licenses_by_dni(dni)
    employee = license_service.get_employee_by_dni(dni)
    
    return jsonify({
        'employee': employee,
        'licenses': licenses,
        'dias_disponibles': int(employee.get('dias_totales', 20)) - int(employee.get('dias_usados', 0)) if employee else 0
    })

@license_bp.route('/active', methods=['GET'])
def get_active_licenses():
    """Get employees currently on leave (active licenses today)"""
    import datetime
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    all_licenses = license_service.get_all_licenses()
    
    # Filtrar licencias activas (donde hoy está entre fecha_inicio y fecha_fin)
    active_licenses = []
    for lic in all_licenses:
        fecha_inicio = lic.get('fecha_inicio', '')
        fecha_fin = lic.get('fecha_fin', '')
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio <= today <= fecha_fin:
                active_licenses.append({
                    'dni': lic.get('dni', ''),
                    'nombres': lic.get('nombres', ''),
                    'apellidos': lic.get('apellidos', ''),
                    'cargo': lic.get('cargo', ''),
                    'area': lic.get('area', ''),
                    'tipo_licencia': lic.get('tipo_licencia', ''),
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'motivo': lic.get('motivo', ''),
                    'dias_restantes': (datetime.datetime.strptime(fecha_fin, '%Y-%m-%d') - 
                                       datetime.datetime.strptime(today, '%Y-%m-%d')).days + 1
                })
    
    return jsonify(active_licenses)
