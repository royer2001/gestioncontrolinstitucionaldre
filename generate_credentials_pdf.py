"""
Script para generar PDF con las credenciales de usuarios del sistema.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch, cm
from datetime import datetime

# Datos de los usuarios de prueba
usuarios = [
    {
        'titulo': '',
        'nombre': 'Juan Carlos Pérez García',
        'dni': '12345671',
        'password': 'vigilante123',
        'rol': 'Vigilante'
    },
    {
        'titulo': '',
        'nombre': 'Miguel Ángel López Torres',
        'dni': '12345672',
        'password': 'vigilante123',
        'rol': 'Vigilante'
    },
    {
        'titulo': '',
        'nombre': 'Roberto Sánchez Medina',
        'dni': '12345673',
        'password': 'vigilante123',
        'rol': 'Vigilante'
    },
    {
        'titulo': '',
        'nombre': 'Fernando José Ramírez Castro',
        'dni': '12345674',
        'password': 'coordinador123',
        'rol': 'Coord. Vigilante'
    },
    {
        'titulo': 'Lic.',
        'nombre': 'María Elena Vargas Rojas',
        'dni': '12345675',
        'password': 'rrhh123',
        'rol': 'Jefe de RRHH'
    },
    {
        'titulo': 'Lic.',
        'nombre': 'Carmen Rosa Díaz Mendoza',
        'dni': '12345676',
        'password': 'bienestar123',
        'rol': 'Jefe de Bienestar'
    },
    {
        'titulo': '',
        'nombre': 'Patricia Luz Fernández Quispe',
        'dni': '12345677',
        'password': 'secretaria123',
        'rol': 'Secretario'
    },
    {
        'titulo': '',
        'nombre': 'Rosa María Huamán Chávez',
        'dni': '12345678',
        'password': 'secretaria123',
        'rol': 'Secretario'
    },
    {
        'titulo': '',
        'nombre': 'Ana Lucía Paredes Valverde',
        'dni': '12345679',
        'password': 'secretaria123',
        'rol': 'Secretario'
    },
    {
        'titulo': 'Dr.',
        'nombre': 'Luis Alberto Morales Ramos',
        'dni': '12345680',
        'password': 'director123',
        'rol': 'Director'
    },
    {
        'titulo': 'Ing.',
        'nombre': 'Carlos Eduardo Vega Salazar',
        'dni': '12345681',
        'password': 'subdirector123',
        'rol': 'Subdirector'
    },
    {
        'titulo': 'CPC.',
        'nombre': 'Jorge Antonio Silva Mendoza',
        'dni': '12345682',
        'password': 'patrimonio123',
        'rol': 'Jefe Patrimonio'
    },
    {
        'titulo': 'Lic.',
        'nombre': 'Pedro Pablo Romero Flores',
        'dni': '12345683',
        'password': 'abastecimiento123',
        'rol': 'Jefe Abastec.'
    },
    {
        'titulo': 'Dra.',
        'nombre': 'Silvia Elena Torres Acuña',
        'dni': '12345684',
        'password': 'oci123',
        'rol': 'Jefe OCI'
    },
]

def generate_pdf():
    # Crear documento
    filename = "credenciales_usuarios_sgci.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                           rightMargin=1.5*cm, leftMargin=1.5*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        alignment=1  # Center
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    elements.append(Paragraph("🏛️ SGCI-DREH", title_style))
    elements.append(Paragraph("Sistema de Gestión y Control Institucional", subtitle_style))
    elements.append(Paragraph("Credenciales de Usuarios de Prueba", styles['Heading2']))
    elements.append(Spacer(1, 20))
    
    # Información
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10,
    )
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", info_style))
    elements.append(Paragraph("⚠️ CONFIDENCIAL - Solo para uso en ambiente de desarrollo", info_style))
    elements.append(Spacer(1, 20))
    
    # Tabla de credenciales
    table_data = [
        ['#', 'Nombre Completo', 'DNI (Usuario)', 'Contraseña', 'Rol']
    ]
    
    for i, user in enumerate(usuarios, 1):
        nombre_completo = f"{user['titulo']} {user['nombre']}".strip() if user['titulo'] else user['nombre']
        table_data.append([
            str(i),
            nombre_completo,
            user['dni'],
            user['password'],
            user['rol']
        ])
    
    # Crear tabla
    col_widths = [0.5*cm, 6.5*cm, 2.5*cm, 3.5*cm, 3*cm]
    table = Table(table_data, colWidths=col_widths)
    
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Body
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        
        # Alignment
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 30))
    
    # Notas
    notes_style = ParagraphStyle(
        'Notes',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#64748b'),
        leftIndent=10,
    )
    
    elements.append(Paragraph("<b>Notas:</b>", styles['Heading3']))
    elements.append(Paragraph("• Estas credenciales son solo para pruebas en ambiente de desarrollo.", notes_style))
    elements.append(Paragraph("• Las contraseñas están hasheadas con SHA256 en la base de datos.", notes_style))
    elements.append(Paragraph("• Para producción, cambiar todas las contraseñas y usar bcrypt.", notes_style))
    elements.append(Paragraph("• URL de acceso: http://localhost:5173/login", notes_style))
    
    # Construir PDF
    doc.build(elements)
    print(f"✅ PDF generado: {filename}")
    return filename

if __name__ == "__main__":
    generate_pdf()
