import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import Config
import datetime
import json
import os

class GoogleSheetsService:
    _instance = None
    _initialized = False
    _client = None
    _creds = None
    _spreadsheet = None
    _worksheets = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleSheetsService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Solo marcar como singleton, NO conectar a Google aún (lazy loading)
        if GoogleSheetsService._initialized:
            return
        
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.sheet_id = Config.GOOGLE_SHEET_ID
        GoogleSheetsService._initialized = True
    
    @property
    def client(self):
        """Lazy loading: solo conecta a Google cuando se necesita"""
        if GoogleSheetsService._client is None:
            print("🔄 Conectando a Google Sheets...")
            
            # Intentar primero desde variable de entorno JSON (para Render)
            if Config.GOOGLE_SHEETS_CREDENTIALS_JSON:
                try:
                    creds_dict = json.loads(Config.GOOGLE_SHEETS_CREDENTIALS_JSON)
                    GoogleSheetsService._creds = ServiceAccountCredentials.from_json_keyfile_dict(
                        creds_dict, self.scope
                    )
                    print("✅ Cargando credenciales desde variable de entorno JSON")
                except Exception as e:
                    print(f"❌ Error al cargar credenciales JSON desde env: {e}")
                    # Fallback al archivo físico si falla
                    GoogleSheetsService._creds = ServiceAccountCredentials.from_json_keyfile_name(
                        Config.GOOGLE_SHEETS_CREDENTIALS_FILE, self.scope
                    )
            else:
                # Fallback al archivo físico
                GoogleSheetsService._creds = ServiceAccountCredentials.from_json_keyfile_name(
                    Config.GOOGLE_SHEETS_CREDENTIALS_FILE, self.scope
                )
                
            GoogleSheetsService._client = gspread.authorize(GoogleSheetsService._creds)
            print("✅ Conexión a Google Sheets establecida")
        return GoogleSheetsService._client

    def get_spreadsheet(self):
        """Obtener el objeto spreadsheet con caché"""
        if GoogleSheetsService._spreadsheet is None:
            GoogleSheetsService._spreadsheet = self.client.open_by_key(self.sheet_id)
        return GoogleSheetsService._spreadsheet

    def get_sheet(self, sheet_name):
        """Obtener el objeto worksheet con caché"""
        if sheet_name not in GoogleSheetsService._worksheets:
            spreadsheet = self.get_spreadsheet()
            GoogleSheetsService._worksheets[sheet_name] = spreadsheet.worksheet(sheet_name)
        return GoogleSheetsService._worksheets[sheet_name]
        
    def ensure_sheet_exists(self, sheet_name, headers=None):
        try:
            self.get_sheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            print(f"Sheet '{sheet_name}' not found. Creating it...")
            sheet = self.client.open_by_key(self.sheet_id)
            worksheet = sheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
            if headers:
                worksheet.append_row(headers)

    def get_all_records(self, sheet_name):
        worksheet = self.get_sheet(sheet_name)
        try:
            return worksheet.get_all_records()
        except Exception as e:
            # Si hay headers duplicados (columnas vacías), construir manualmente
            if 'duplicates' in str(e):
                all_values = worksheet.get_all_values()
                if not all_values:
                    return []
                
                headers = all_values[0]
                # Filtrar headers vacíos y crear nombres únicos para duplicados
                clean_headers = []
                seen = {}
                for i, h in enumerate(headers):
                    if not h or h.strip() == '':
                        continue  # Ignorar columnas sin header
                    if h in seen:
                        seen[h] += 1
                        clean_headers.append((i, f"{h}_{seen[h]}"))
                    else:
                        seen[h] = 0
                        clean_headers.append((i, h))
                
                records = []
                for row in all_values[1:]:
                    record = {}
                    for col_idx, header_name in clean_headers:
                        if col_idx < len(row):
                            record[header_name] = row[col_idx]
                        else:
                            record[header_name] = ''
                    records.append(record)
                return records
            else:
                raise e

    def get_all_values(self, sheet_name):
        worksheet = self.get_sheet(sheet_name)
        return worksheet.get_all_values()

    def append_row(self, sheet_name, row_data):
        worksheet = self.get_sheet(sheet_name)
        worksheet.append_row(row_data)

    def update_cell(self, sheet_name, row, col, value):
        worksheet = self.get_sheet(sheet_name)
        worksheet.update_cell(row, col, value)

    def log_audit(self, user, action, details, occurrence_id=None):
        row_data = [
            int(datetime.datetime.now().timestamp()),
            user,
            occurrence_id if occurrence_id else '',
            action,
            details,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        try:
            self.append_row('historial_cambios', row_data)
        except:
             pass 

    def find_by_value(self, sheet_name, column_name, value):
        try:
            records = self.get_all_records(sheet_name)
            for record in records:
                # Convert both to string to ensure matching works
                if str(record.get(column_name, '')) == str(value):
                    return record
            return None
        except Exception as e:
            print(f"Error searching in {sheet_name}: {e}")
            return None

    def find_row_index_by_value(self, sheet_name, value, col_index=None):
        try:
            worksheet = self.get_sheet(sheet_name)
            if col_index:
                cell = worksheet.find(str(value), in_column=col_index)
            else:
                cell = worksheet.find(str(value))
            return cell.row if cell else None
        except Exception as e:
            print(f"Error finding row in {sheet_name}: {e}")
            return None

    def get_row_by_index(self, sheet_name, row_index):
        """Get all values from a specific row by its index (1-based)"""
        try:
            worksheet = self.get_sheet(sheet_name)
            return worksheet.row_values(row_index)
        except Exception as e:
            print(f"Error getting row {row_index} from {sheet_name}: {e}")
            return None
