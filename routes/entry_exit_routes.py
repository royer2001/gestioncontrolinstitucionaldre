from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash, send_file
from services.google_sheets import GoogleSheetsService
import datetime
import io
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors

entry_exit_bp = Blueprint('entry_exit', __name__)
sheets_service = GoogleSheetsService()

@entry_exit_bp.route('/generate_pdf/<entry_id>', methods=['GET'])
def generate_pdf(entry_id):
    try:
        # Buscar el registro
        row_index = sheets_service.find_row_index_by_value('entradas_salidas', entry_id, col_index=1)
        if not row_index:
            return jsonify({'message': 'Registro no encontrado'}), 404
            
        # Obtener datos de la fila
        rows = sheets_service.get_all_values('entradas_salidas')
        # row_index es 1-based, rows es 0-based list. row_index 2 es rows[1]
        row_data = rows[row_index - 1]
        
        # Mapear datos (según estructura conocida)
        # ['entry_id', 'personal', 'hora_entrada', 'hora_salida', 'motivo', 'papeleta', 'usuario', 'fecha', 'turno', 'regimen']
        entry = {
            'personal': row_data[1],
            'hora_salida': row_data[3],
            'motivo': row_data[4],
            'papeleta': row_data[5],
            'fecha': row_data[7],
            'regimen': row_data[9] if len(row_data) > 9 else ''
        }
        
        # Buscar DNI en hoja personal o usuarios para completar datos
        dni = ''
        # Primero intentar obtener el DNI directamente del registro si existe (columna 10, índice 10)
        if len(row_data) > 10 and row_data[10]:
            dni = row_data[10]
        else:
            # Fallback: buscar en hoja personal o usuarios
            personal_record = sheets_service.find_by_value('personal', 'Nombre', entry['personal'])
            if not personal_record:
                 personal_record = sheets_service.find_by_value('usuarios', 'Nombre', entry['personal'])
            
            if personal_record:
                dni = personal_record.get('DNI', '')

        # Crear PDF en memoria - Tamaño A5 (148mm x 210mm)
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A5)
        width, height = A5
        
        # --- Encabezado ---
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 1.2 * cm, "PAPELETA DE SALIDA DE PERSONAL")
        
        c.setFont("Helvetica", 8)
        c.drawCentredString(width / 2, height - 1.8 * cm, "DIRECCIÓN REGIONAL DE EDUCACIÓN HUÁNUCO")
        
        # --- Recuadro de Datos ---
        c.setLineWidth(1)
        c.rect(1 * cm, height - 8 * cm, width - 2 * cm, 5.5 * cm)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1.5 * cm, height - 3 * cm, f"N° PAPELETA: {entry['papeleta']}")
        c.drawString(8 * cm, height - 3 * cm, f"FECHA: {entry['fecha']}")
        
        c.setFont("Helvetica-Bold", 9)
        y_start = height - 4 * cm
        line_height = 0.7 * cm
        
        c.drawString(1.5 * cm, y_start, "APELLIDOS Y NOMBRES:")
        c.setFont("Helvetica", 9)
        # Truncar nombre si es muy largo
        nombre = entry['personal'][:35] if len(entry['personal']) > 35 else entry['personal']
        c.drawString(5.5 * cm, y_start, nombre)
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(1.5 * cm, y_start - line_height, "DNI:")
        c.setFont("Helvetica", 9)
        c.drawString(5.5 * cm, y_start - line_height, str(dni))
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(8 * cm, y_start - line_height, "RÉGIMEN:")
        c.setFont("Helvetica", 9)
        c.drawString(10.2 * cm, y_start - line_height, entry['regimen'])
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(1.5 * cm, y_start - 2 * line_height, "MOTIVO:")
        c.setFont("Helvetica", 9)
        # Manejo básico de texto largo para motivo
        motivo = entry['motivo']
        if len(motivo) > 40:
            motivo = motivo[:40] + "..."
        c.drawString(5.5 * cm, y_start - 2 * line_height, motivo)
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(1.5 * cm, y_start - 3 * line_height, "HORA SALIDA:")
        c.setFont("Helvetica", 9)
        c.drawString(5.5 * cm, y_start - 3 * line_height, entry['hora_salida'])
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(8 * cm, y_start - 3 * line_height, "HORA RETORNO:")
        c.setFont("Helvetica", 9)
        c.drawString(10.8 * cm, y_start - 3 * line_height, "__________")

        # --- Firmas ---
        y_firmas_row1 = height - 10 * cm
        y_firmas_row2 = height - 12.5 * cm
        
        c.setLineWidth(0.5)
        # Fila 1: Dos firmas lado a lado
        # Firma 1 - SERVIDOR (izquierda)
        c.line(1.5 * cm, y_firmas_row1, 6 * cm, y_firmas_row1)
        c.setFont("Helvetica", 7)
        c.drawCentredString(3.75 * cm, y_firmas_row1 - 0.4 * cm, "FIRMA DEL SERVIDOR")
        
        # Firma 2 - JEFE INMEDIATO (derecha)
        c.line(8 * cm, y_firmas_row1, 12.5 * cm, y_firmas_row1)
        c.drawCentredString(10.25 * cm, y_firmas_row1 - 0.4 * cm, "JEFE INMEDIATO")
        
        # Fila 2: Una firma centrada abajo
        # Firma 3 - VISTO BUENO (centrado)
        firma_center = width / 2
        c.line(firma_center - 2.5 * cm, y_firmas_row2, firma_center + 2.5 * cm, y_firmas_row2)
        c.drawCentredString(firma_center, y_firmas_row2 - 0.4 * cm, "VISTO BUENO (DESTINO)")
        
        c.save()
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=False,
            download_name=f"papeleta_{entry['papeleta']}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({'message': 'Error generando PDF'}), 500


@entry_exit_bp.route('/list')
def list_entries():
    # Obtener todos los valores como lista de listas para mapeo manual
    # Esto evita problemas si faltan encabezados en Google Sheets
    rows = sheets_service.get_all_values('entradas_salidas')
    
    entries = []
    if len(rows) > 1: # Si hay más que solo la fila de encabezados (o vacía)
        # Asumimos que la fila 0 son encabezados, empezamos desde la 1
        data_rows = rows[1:]
        
        # Invertir orden para mostrar los más recientes primero (opcional, pero útil)
        data_rows.reverse()
        
        for row in data_rows:
            # Asegurar que la fila tenga suficientes columnas (rellenar con '')
            # Esperamos 11 columnas (índice 0 a 10)
            while len(row) < 11:
                row.append('')
            
            # Mapeo manual basado en el orden de inserción en register()
            entry = {
                'entry_id': row[0],
                'personal': row[1],
                'hora_entrada': row[2],
                'hora_salida': row[3],
                'motivo': row[4],
                'papeleta': row[5],
                'usuario_registro': row[6],
                'fecha': row[7],
                'turno': row[8],
                'tipo_regimen': row[9],
                'dni': row[10]
            }
            entries.append(entry)
            
    return jsonify(entries), 200

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

@entry_exit_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(f"DEBUG REGISTER PAYLOAD: {data}", flush=True)
    username = data.get('username', 'unknown')
    action = data.get('action', 'salida') # 'salida' (crear) o 'retorno' (actualizar)

    if action == 'retorno':
        entry_id = data.get('entry_id')
        hora_retorno = data.get('hora_entrada')
        
        if not entry_id:
            return jsonify({'message': 'Falta entry_id para registrar retorno'}), 400

        # Buscar fila por entry_id (columna 1)
        row = sheets_service.find_row_index_by_value('entradas_salidas', entry_id, col_index=1)
        
        if row:
            # Actualizar columna 3 (hora_entrada/retorno)
            sheets_service.update_cell('entradas_salidas', row, 3, hora_retorno)
            sheets_service.log_audit(username, 'Registrar Retorno', f"Retorno registrado para entry_id {entry_id}")
            return jsonify({'message': 'Retorno registrado exitosamente'}), 200
        else:
            return jsonify({'message': 'Registro original no encontrado'}), 404

    else:
        # Registrar Salida (Nuevo registro)
        entry_id = int(datetime.datetime.now().timestamp())
        shift = get_shift()

        # Generar número de papeleta correlativo
        papeleta_number = '000001'
        try:
            rows = sheets_service.get_all_values('entradas_salidas')
            if len(rows) > 1:
                # Extraer números de papeleta existentes (columna 5, índice 5)
                papeletas = []
                for r in rows[1:]:
                    # Ahora esperamos solo números o cadenas vacías
                    if len(r) > 5 and r[5] and r[5].isdigit():
                        papeletas.append(int(r[5]))
                
                if papeletas:
                    next_num = max(papeletas) + 1
                    papeleta_number = f"{next_num:06d}"
        except Exception as e:
            print(f"Error generating papeleta number: {e}")
            # Fallback a timestamp si falla la generación correlativa
            papeleta_number = f"{int(datetime.datetime.now().timestamp())}"

        row_data = [
            entry_id,
            data.get('personal'),
            '', # hora_entrada (Retorno) vacía al salir
            data.get('hora_salida'),
            data.get('motivo'),
            papeleta_number, # Auto-generated papeleta
            username,
            datetime.datetime.now().strftime("%Y-%m-%d"),
            shift,
            data.get('tipo_regimen', ''),
            data.get('dni', '') # Add DNI to the row data
        ]
        
        sheets_service.append_row('entradas_salidas', row_data)
        sheets_service.log_audit(username, 'Registrar Salida', f"Salida registrada {entry_id} en turno {shift} con papeleta {papeleta_number}")
        return jsonify({'message': 'Salida registrada exitosamente', 'papeleta': papeleta_number, 'entry_id': entry_id}), 201

@entry_exit_bp.route('/search_personal/<dni>', methods=['GET'])
def search_personal(dni):
    # Search in 'personal' sheet first
    record = sheets_service.find_by_value('personal', 'DNI', dni)
    
    if not record:
        record = sheets_service.find_by_value('usuarios', 'DNI', dni)

    if record:
        nombre = record.get('Nombre') or record.get('Nombres') or f"{record.get('Nombre', '')} {record.get('Apellido', '')}".strip()
        if not nombre:
             nombre = record.get('usuario', '')
        
        # Verificar estado actual
        status_data = {'status': 'dentro'} # Default
        try:
            # Usar get_all_values para mapeo manual consistente
            rows = sheets_service.get_all_values('entradas_salidas')
            entries = []
            if len(rows) > 1:
                data_rows = rows[1:]
                for row in data_rows:
                    while len(row) < 10:
                        row.append('')
                    entries.append({
                        'entry_id': row[0],
                        'personal': row[1],
                        'hora_entrada': row[2],
                        'hora_salida': row[3],
                        'motivo': row[4],
                        'papeleta': row[5],
                        'usuario_registro': row[6],
                        'fecha': row[7],
                        'turno': row[8],
                        'tipo_regimen': row[9]
                    })

            # Filtrar registros de este personal
            personal_entries = [e for e in entries if str(e.get('personal')) == str(nombre)]
            
            if personal_entries:
                last_entry = personal_entries[-1]
                # Si tiene salida pero no entrada (retorno), está fuera
                if last_entry.get('hora_salida') and not last_entry.get('hora_entrada'):
                    status_data = {
                        'status': 'fuera',
                        'entry_id': last_entry.get('entry_id'),
                        'hora_salida': last_entry.get('hora_salida'),
                        'motivo': last_entry.get('motivo'),
                        'tipo_regimen': last_entry.get('tipo_regimen')
                    }
        except Exception as e:
            print(f"Error checking status: {e}")

        return jsonify({
            'nombre': nombre,
            **status_data
        }), 200
    else:
        return jsonify({'message': 'Personal no encontrado'}), 404


