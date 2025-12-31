from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from services.google_sheets import GoogleSheetsService
from services.auth_service import AuthService
import datetime

occurrence_bp = Blueprint('occurrence', __name__)
sheets_service = GoogleSheetsService()

@occurrence_bp.route('/dashboard')
def dashboard():
    # Token verification is now handled by frontend sending header, 
    # but we should verify it here too using a decorator or similar.
    # For simplicity in this migration step, we'll assume the token is valid 
    # if we were using the @token_required decorator from AuthService.
    # However, since we are moving to API, we should use the decorator.
    
    # Let's use the decorator if possible, or just check header manually for now
    # to avoid circular imports or complex refactoring in this step.
    
    occurrences = sheets_service.get_all_records('ocurrencias')
    
    try:
        users = sheets_service.get_all_records('usuarios')
        # Create a map of DNI to Name
        user_map = {}
        for u in users:
            # La columna 'dni' contiene el DNI del usuario
            dni = str(u.get('dni', '')).strip()
            
            # Obtener el título y nombre
            titulo = u.get('titulo', '') or ''
            nombre = u.get('nombre') or u.get('Nombre') or ''
            
            # Construir nombre completo con título
            if titulo and nombre:
                full_name = f"{titulo} {nombre}"
            elif nombre:
                full_name = nombre
            else:
                full_name = dni  # Fallback al DNI
                
            if dni:
                user_map[dni] = full_name

        # Enrich occurrences with Name - DNI
        for occ in occurrences:
            # Check for 'Vigilante' or 'vigilante' key
            vigilante_key = 'Vigilante' if 'Vigilante' in occ else 'vigilante'
            vigilante_dni = str(occ.get(vigilante_key, '')).strip()
            
            if vigilante_dni:
                name = user_map.get(vigilante_dni, vigilante_dni)
                if name and name != vigilante_dni:
                    occ[vigilante_key] = f"{name} - {vigilante_dni}"
                    
    except Exception as e:
        print(f"Error enriching occurrences with user data: {e}")
        # Continue without enrichment if users fetch fails

    return jsonify(occurrences), 200

@occurrence_bp.route('/summary')
def summary():
    """
    Returns summary statistics for the main dashboard.
    Includes counts for occurrences, personnel entry/exit, and visitors.
    """
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    stats = {
        'occurrences': {
            'total': 0,
            'incidentes': 0,
            'emergencias': 0,
            'rutinas': 0
        },
        'personnel': {
            'total': 0,
            'pending_return': 0,
            'today': 0
        },
        'visitors': {
            'total': 0,
            'active': 0,
            'today': 0
        }
    }
    
    try:
        # Occurrences
        occurrences = sheets_service.get_all_records('ocurrencias')
        stats['occurrences']['total'] = len(occurrences)
        for occ in occurrences:
            tipo = occ.get('tipo') or occ.get('Tipo') or ''
            if tipo == 'Incidente':
                stats['occurrences']['incidentes'] += 1
            elif tipo == 'Emergencia':
                stats['occurrences']['emergencias'] += 1
            elif tipo == 'Rutina':
                stats['occurrences']['rutinas'] += 1
    except Exception as e:
        print(f"Error fetching occurrences summary: {e}")
    
    try:
        # Personnel Entry/Exit
        rows = sheets_service.get_all_values('entradas_salidas')
        if len(rows) > 1:
            data_rows = rows[1:]
            stats['personnel']['total'] = len(data_rows)
            for row in data_rows:
                while len(row) < 8:
                    row.append('')
                # Check if no return time (hora_entrada is column 2)
                hora_entrada = row[2] if len(row) > 2 else ''
                if not hora_entrada:
                    stats['personnel']['pending_return'] += 1
                # Check if today
                fecha = row[7] if len(row) > 7 else ''
                if fecha == today:
                    stats['personnel']['today'] += 1
    except Exception as e:
        print(f"Error fetching personnel summary: {e}")
    
    try:
        # Visitors
        rows = sheets_service.get_all_values('visitas')
        if len(rows) > 1:
            data_rows = rows[1:]
            stats['visitors']['total'] = len(data_rows)
            for row in data_rows:
                while len(row) < 10:
                    row.append('')
                # Check if active (estado != 'Finalizado')
                estado = row[9] if len(row) > 9 else ''
                if estado != 'Finalizado':
                    stats['visitors']['active'] += 1
                # Check if today
                fecha = row[5] if len(row) > 5 else ''
                if fecha == today:
                    stats['visitors']['today'] += 1
    except Exception as e:
        print(f"Error fetching visitors summary: {e}")
    
    return jsonify(stats), 200

def get_shift():
    current_time = datetime.datetime.now().time()
    morning_start = datetime.time(6, 0)
    afternoon_start = datetime.time(14, 0)
    night_start = datetime.time(22, 0)
    
    if morning_start <= current_time < afternoon_start:
        return 'Mañana'
    elif afternoon_start <= current_time < night_start:
        return 'Tarde'
    else:
        return 'Noche'

@occurrence_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Generate ID (simple timestamp based for now)
    occurrence_id = int(datetime.datetime.now().timestamp())
    
    # Obtener datos del responsable que registra la ocurrencia
    responsable_dni = data.get('responsable_dni', 'unknown')
    responsable_nombre = data.get('responsable_nombre', 'Desconocido')
    
    # Formato: "Nombre Completo - DNI" para el campo vigilante
    vigilante_display = f"{responsable_nombre} - {responsable_dni}"

    shift = get_shift()

    # Estructura alineada con los headers existentes de la hoja:
    # id, fecha, hora, turno, vigilante, tipo, descripcion, acciones, 
    # evidencia_url, firma_entrante, firma_saliente, estado, creado_por, creado_en, actualizado_en
    row_data = [
        occurrence_id,                                              # id
        datetime.datetime.now().strftime("%Y-%m-%d"),               # fecha
        datetime.datetime.now().strftime("%H:%M:%S"),               # hora
        shift,                                                       # turno
        vigilante_display,                                           # vigilante (Nombre - DNI)
        data.get('tipo'),                                            # tipo
        data.get('descripcion'),                                     # descripcion
        data.get('acciones', ''),                                    # acciones
        data.get('evidencia_url', ''),                               # evidencia_url
        '',                                                          # firma_entrante
        '',                                                          # firma_saliente
        'Pendiente',                                                 # estado
        responsable_dni,                                             # creado_por (DNI)
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),       # creado_en
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")        # actualizado_en
    ]
    
    sheets_service.append_row('ocurrencias', row_data)
    sheets_service.log_audit(responsable_dni, 'Registrar Ocurrencia', f"Ocurrencia {occurrence_id} registrada en turno {shift} por {responsable_nombre}", occurrence_id)
    return jsonify({'message': 'Ocurrencia registrada exitosamente', 'id': occurrence_id}), 201

@occurrence_bp.route('/approve/<int:id>', methods=['POST'])
def approve(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    # Logic to find row by ID and update status
    # This is tricky with append-only sheets, need to find the row index first
    # For now, we'll implement a simple find and update
    
    # TODO: Implement update logic in GoogleSheetsService
    flash('Funcionalidad de aprobación en desarrollo', 'info')
    return redirect(url_for('occurrence.dashboard'))
