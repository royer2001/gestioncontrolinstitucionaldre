from flask import Blueprint, make_response, session, redirect, url_for
from services.google_sheets import GoogleSheetsService
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import datetime

report_bp = Blueprint('report', __name__)
sheets_service = GoogleSheetsService()

@report_bp.route('/generate_pdf')
def generate_pdf():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    occurrences = sheets_service.get_all_records('ocurrencias')
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Reporte de Ocurrencias - DRE Huánuco")
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Generado el: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    y = height - 100
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Fecha")
    p.drawString(120, y, "Hora")
    p.drawString(180, y, "Tipo")
    p.drawString(250, y, "Descripción")
    p.drawString(450, y, "Vigilante")
    
    y -= 20
    p.setFont("Helvetica", 9)
    
    for occ in occurrences:
        if y < 50:
            p.showPage()
            y = height - 50
            
        p.drawString(50, y, str(occ.get('fecha', '')))
        p.drawString(120, y, str(occ.get('hora', '')))
        p.drawString(180, y, str(occ.get('tipo', '')))
        # Truncate description for PDF
        desc = str(occ.get('descripcion', ''))
        if len(desc) > 40:
            desc = desc[:37] + "..."
        p.drawString(250, y, desc)
        p.drawString(450, y, str(occ.get('vigilante', '')))
        y -= 15
        
    p.save()
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_ocurrencias.pdf'
    
    return response
