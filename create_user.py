import hashlib
from services.google_sheets import GoogleSheetsService
import gspread

def create_admin_user():
    service = GoogleSheetsService()
    
    # Define required sheets and their headers
    required_sheets = {
        'usuarios': ['id', 'nombre', 'usuario', 'contraseña_hash', 'rol'],
        'ocurrencias': ['id', 'fecha', 'hora', 'turno', 'vigilante', 'tipo', 'descripcion', 'acciones', 'evidencia_url', 'firma_entrante', 'firma_saliente', 'estado', 'creado_por', 'creado_en', 'actualizado_en'],
        'entradas_salidas': ['id', 'personal', 'hora_entrada', 'hora_salida', 'motivo', 'papeleta', 'vigilante', 'fecha'],
        'visitas': ['id', 'nombre_visitante', 'dni', 'area', 'motivo', 'fecha', 'hora_entrada', 'hora_salida', 'registrado_por', 'estado'],
        'historial_cambios': ['id', 'usuario', 'ocurrencia_id', 'accion', 'detalle', 'fecha']
    }
    
    spreadsheet = service.client.open_by_key(service.sheet_id)
    
    for sheet_name, headers in required_sheets.items():
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            print(f"Sheet '{sheet_name}' already exists.")
        except gspread.exceptions.WorksheetNotFound:
            print(f"Sheet '{sheet_name}' not found. Creating...")
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
            worksheet.append_row(headers)
            print(f"Created '{sheet_name}' with headers.")

    # Now add the user
    sheet_name = 'usuarios'
    username = "12345678" # DNI Example
    password = "admin123"
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    records = service.get_all_records(sheet_name)
    for record in records:
        if str(record['usuario']) == username:
            print(f"User '{username}' already exists.")
            return

    new_id = len(records) + 1
    
    user_data = [
        new_id,
        "Administrador Principal",
        username,
        password_hash,
        "admin"
    ]
    
    print(f"Creating user: {username} with password: {password}")
    service.append_row(sheet_name, user_data)
    print("User created successfully in Google Sheets.")

if __name__ == "__main__":
    create_admin_user()
