from flask import Blueprint, request, jsonify, send_file
from services.google_sheets import GoogleSheetsService
import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

visitor_bp = Blueprint('visitor', __name__)
sheets_service = GoogleSheetsService()

@visitor_bp.route('/areas', methods=['GET'])
def get_areas():
    areas = [
        "Dirección Regional",
        "Administración",
        "Gestión Pedagógica",
        "Gestión Institucional",
        "Recursos Humanos",
        "Asesoría Jurídica",
        "Órgano de Control Institucional",
        "Mesa de Partes",
        "Trámite Documentario",
        "Tesorería",
        "Contabilidad",
        "Abastecimiento",
        "Patrimonio"
    ]
    return jsonify(areas), 200

@visitor_bp.route('/register', methods=['POST'])
def register_visitor():
    data = request.get_json()
    username = data.get('username', 'unknown')
    
    # Visit data
    visitor_name = data.get('visitor_name')
    dni = data.get('dni')
    area = data.get('area')
    reason = data.get('reason')
    
    # Validation
    if not visitor_name or not dni or not area:
        return jsonify({'message': 'Faltan datos obligatorios'}), 400

    entry_id = int(datetime.datetime.now().timestamp())
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    
    row_data = [
        entry_id,
        visitor_name,
        dni,
        area,
        reason,
        fecha,
        hora, # Hora Entrada
        '',   # Hora Salida (Empty initially)
        username,
        'En curso' # Estado
    ]
    
    try:
        sheets_service.append_row('visitas', row_data)
        sheets_service.log_audit(username, 'Registrar Visita', f"Visita registrada para {visitor_name} en {area}")
        return jsonify({'message': 'Visita registrada exitosamente', 'entry_id': entry_id}), 201
    except Exception as e:
        print(f"Error registering visitor: {e}")
        return jsonify({'message': 'Error al registrar visita. Verifique que la hoja "visitas" exista.'}), 500

@visitor_bp.route('/list', methods=['GET'])
def list_visitors():
    try:
        rows = sheets_service.get_all_values('visitas')
        if len(rows) > 1:
            data_rows = rows[1:]
            data_rows.reverse() # Show newest first
            
            visitors = []
            for row in data_rows:
                # Ensure row has enough columns
                while len(row) < 10:
                    row.append('')
                    
                visitors.append({
                    'entry_id': row[0],
                    'visitor_name': row[1],
                    'dni': row[2],
                    'area': row[3],
                    'reason': row[4],
                    'fecha': row[5],
                    'hora_entrada': row[6],
                    'hora_salida': row[7],
                    'usuario': row[8],
                    'estado': row[9]
                })
            return jsonify(visitors), 200
        return jsonify([]), 200
    except Exception as e:
         print(f"Error listing visitors: {e}")
         return jsonify([]), 500

@visitor_bp.route('/checkout', methods=['POST'])
def checkout_visitor():
    data = request.get_json()
    entry_id = data.get('entry_id')
    username = data.get('username', 'unknown')
    
    if not entry_id:
        return jsonify({'message': 'Falta entry_id'}), 400
        
    row = sheets_service.find_row_index_by_value('visitas', entry_id, col_index=1)
    
    if row:
        hora_salida = datetime.datetime.now().strftime("%H:%M:%S")
        sheets_service.update_cell('visitas', row, 8, hora_salida) # Update Hora Salida
        sheets_service.update_cell('visitas', row, 10, 'Finalizado') # Update Estado
        
        sheets_service.log_audit(username, 'Finalizar Visita', f"Salida registrada para visita ID {entry_id}")
        return jsonify({'message': 'Salida de visita registrada'}), 200
    else:
        return jsonify({'message': 'Visita no encontrada'}), 404

@visitor_bp.route('/ticket/<entry_id>', methods=['GET'])
def generate_visitor_ticket(entry_id):
    try:
        # 1. Obtener todos los valores y buscar localmente para reducir llamadas API
        rows = sheets_service.get_all_values('visitas')
        if not rows or len(rows) <= 1:
            return jsonify({'message': 'No hay datos de visitas'}), 404
            
        row_data = None
        # Buscar el ID en la primera columna (índice 0)
        for row in rows[1:]:
            if str(row[0]) == str(entry_id):
                row_data = row
                break
                
        if not row_data:
            return jsonify({'message': 'Visita no encontrada'}), 404
            
        # Mapping columns based on register_visitor:
        # 0:id, 1:name, 2:dni, 3:area, 4:reason, 5:fecha, 6:hora, 7:salida, 8:user, 9:estado
        visitor = {
            'name': row_data[1] if len(row_data) > 1 else 'Desconocido',
            'dni': row_data[2] if len(row_data) > 2 else '-',
            'area': row_data[3] if len(row_data) > 3 else '-',
            'reason': row_data[4] if len(row_data) > 4 else '-',
            'fecha': row_data[5] if len(row_data) > 5 else '',
            'hora': row_data[6] if len(row_data) > 6 else ''
        }
        
        # Convert fecha from YYYY-MM-DD to DD/MM/YYYY
        try:
             date_obj = datetime.datetime.strptime(visitor['fecha'], "%Y-%m-%d")
             formatted_date = date_obj.strftime("%d/%m/%Y")
        except ValueError:
             formatted_date = visitor['fecha'] # Fallback if format is different

        # Convert hora from HH:MM:SS to HH:MM am/pm
        try:
             time_obj = datetime.datetime.strptime(visitor['hora'], "%H:%M:%S")
             formatted_time = time_obj.strftime("%I:%M %p").lower()
        except ValueError:
             formatted_time = listener['hora'] # Fallback

        # 2. Configuración del PDF (Ticket térmico 80mm)
        # 80mm = ~3.15 inches. Height is dynamic but we start with a fixed helpful height or A6
        ticket_width = 8 * cm
        # Calculamos altura aproximada necesaria
        ticket_height = 15 * cm 
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(ticket_width, ticket_height))
        
        # Configuración de márgenes y posiciones
        margin_left = 0.5 * cm
        width = ticket_width
        y = ticket_height - 1 * cm
        
        # --- Contenido del Ticket ---
        
        # 1. Encabezado: Logo y Título (Side by side)
        logo_path = 'assets/logo.png'
        logo_width = 1.1 * cm
        logo_height = 1.1 * cm
        
        # Textos
        # Ajustamos el tamaño de fuente y dividimos en líneas para que quepa
        c.setFont("Helvetica-Bold", 7)
        line1 = "BIENVENIDO A LA"
        c.setFont("Helvetica-Bold", 8)
        line2 = "DIRECCIÓN REGIONAL DE"
        line3 = "EDUCACIÓN - HUÁNUCO"
        
        # Calculate centering based on widest line
        w1 = c.stringWidth(line1, "Helvetica-Bold", 7)
        w2 = c.stringWidth(line2, "Helvetica-Bold", 8)
        w3 = c.stringWidth(line3, "Helvetica-Bold", 8)
        max_text_width = max(w1, w2, w3)
        
        gap = 0.2 * cm
        total_header_width = logo_width + gap + max_text_width
        start_x = (width - total_header_width) / 2
        
        try:
            # Draw Logo
            current_y_logo = y
            # Logo centrado verticalmente respecto a las 3 líneas de texto (aprox 1cm de altura total texto)
            # Logo es 1.1cm.
            c.drawImage(logo_path, start_x, current_y_logo - logo_height, width=logo_width, height=logo_height, mask='auto')
        except Exception as e:
            print(f"Warning: Logo not found or error loading: {e}")
            
        # Draw Text
        text_x = start_x + logo_width + gap
        
        # Line spacing
        line_height = 0.35 * cm
        
        # Vertical alignment correction
        # Logo height 1.1 cm. Center is at y - 0.55cm.
        # Text block (3 lines) center should align with that.
        # Line 2 is the middle line.
        # We want Line 2's visual center roughly at y - 0.55cm.
        # Line 2 baseline ~ y - 0.65cm.
        
        text_start_y = y - 0.3 * cm
        
        c.setFont("Helvetica-Bold", 7)
        c.drawString(text_x + (max_text_width - w1)/2, text_start_y, line1)
        
        c.setFont("Helvetica-Bold", 8)
        c.drawString(text_x + (max_text_width - w2)/2, text_start_y - line_height, line2)
        c.drawString(text_x + (max_text_width - w3)/2, text_start_y - 2*line_height, line3)
        
        y -= (logo_height + 0.5 * cm)

        # 2. Fecha y Hora
        c.setFont("Helvetica", 9)
        c.drawCentredString(width / 2, y, f"{formatted_date} - {formatted_time}")
        y -= 0.8 * cm

        # 4. ID Ticket
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, y, f"TICKET #: {entry_id}")
        y -= 0.8 * cm
        
        # Separador
        c.setLineWidth(0.5)
        c.line(margin_left, y, width - margin_left, y)
        y -= 0.8 * cm
        
        # 5. Detalles de la Visita
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin_left, y, "VISITANTE:")
        y -= 0.5 * cm
        c.setFont("Helvetica", 9)
        # Wrap simple si el nombre es muy largo
        name = visitor['name']
        if len(name) > 25:
             c.drawString(margin_left, y, name[:25])
             y -= 0.4 * cm
             c.drawString(margin_left, y, name[25:])
        else:
             c.drawString(margin_left, y, name)
        y -= 0.6 * cm
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin_left, y, f"DNI: {visitor['dni']}")
        y -= 0.6 * cm
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin_left, y, "ÁREA:")
        y -= 0.4 * cm
        c.setFont("Helvetica", 9)
        # Wrap Area
        area = visitor['area']
        if len(area) > 25:
             c.drawString(margin_left, y, area[:25])
             y -= 0.4 * cm
             c.drawString(margin_left, y, area[25:])
        else:
            c.drawString(margin_left, y, area)
        y -= 1.5 * cm
        
        # 6. Pie de Página
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(width / 2, y, "Conserve este ticket")
        
        c.showPage()
        c.save()
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=False, # False para que se abra en el navegador y sea fácil imprimir
            download_name=f"ticket_{entry_id}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating ticket: {e}")
        return jsonify({'message': 'Error generando ticket'}), 500
