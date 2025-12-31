from services.google_sheets import GoogleSheetsService
import datetime
import uuid
import json

class CitaService:
    _sheets_ready = False
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.sheet_name = 'citas'
        # NOTA: NO llamar _ensure_sheets_ready() aquí para evitar conexión en import

    def _ensure_sheets_ready(self):
        headers = [
            'id', 'dni', 'oficina', 'apellidos', 'nombres', 'fecha', 
            'celular', 'hora', 'correo', 'asunto', 'estado', 'historial_json', 'created_at'
        ]
        if not CitaService._sheets_ready:
            self.sheets_service.ensure_sheet_exists(self.sheet_name, headers)
            CitaService._sheets_ready = True

    def create_cita(self, data):
        self._ensure_sheets_ready()
        cita_id = str(uuid.uuid4())
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Initial history entry
        historial = [
            {'estado': 'PENDIENTE', 'fecha': now, 'descripcion': 'Cita registrada'}
        ]
        
        row_data = [
            cita_id,
            data.get('dni', ''),
            data.get('oficina', ''),
            data.get('apellidos', ''),
            data.get('nombres', ''),
            data.get('fecha', ''),
            data.get('celular', ''),
            data.get('hora', ''),
            data.get('correo', ''),
            data.get('asunto', ''),
            'PENDIENTE',
            json.dumps(historial),
            now
        ]
        self.sheets_service.append_row(self.sheet_name, row_data)
        return cita_id

    def get_all_citas(self):
        self._ensure_sheets_ready()
        try:
            records = self.sheets_service.get_all_records(self.sheet_name)
            # Parse historial JSON - check multiple possible locations due to column mismatch
            for r in records:
                historial_parsed = []
                
                # Try historial_json column first
                if 'historial_json' in r and r['historial_json']:
                    try:
                        historial_parsed = json.loads(r['historial_json'])
                    except:
                        pass
                
                # If that failed, check created_at (in case columns shifted)
                if not historial_parsed and 'created_at' in r and r['created_at']:
                    try:
                        content = str(r['created_at'])
                        if content.startswith('[{'):
                            historial_parsed = json.loads(content)
                    except:
                        pass
                
                r['historial'] = historial_parsed
            return records
        except Exception as e:
            print(f"Error fetching citas: {e}")
            return []

    def get_citas_by_dni(self, dni):
        try:
            all_records = self.get_all_citas()  # Use the method that parses historial
            dni_str = str(dni).strip()
            result = [r for r in all_records if str(r.get('dni', '')).strip() == dni_str]
            print(f"Searching for DNI: {dni_str}, found {len(result)} records")
            return result
        except Exception as e:
            print(f"Error fetching citas by dni: {e}")
            return []

    def update_cita_status(self, cita_id, new_status, observacion=None):
        try:
            row_index = self.sheets_service.find_row_index_by_value(self.sheet_name, cita_id, col_index=1)
            if not row_index:
                return False
            
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Get current historial
            current_row = self.sheets_service.get_row_by_index(self.sheet_name, row_index)
            historial = []
            if current_row and len(current_row) > 11:
                try:
                    historial = json.loads(current_row[11]) if current_row[11] else []
                except:
                    historial = []
            
            # Add new status entry
            default_descripcion_map = {
                'ATENDIDO': 'Cita atendida',
                'CANCELADO': 'Cita cancelada',
                'PENDIENTE': 'Estado cambiado a pendiente'
            }
            
            # Use provided observation or default if none given
            final_descripcion = observacion if observacion else default_descripcion_map.get(new_status, f'Estado cambiado a {new_status}')

            historial.append({
                'estado': new_status,
                'fecha': now,
                'descripcion': final_descripcion
            })
            
            # Update estado (col 11) and historial_json (col 12)
            print(f"Updating Cita {cita_id}: status={new_status}, observacion={observacion}")
            print(f"New historial: {historial}")
            
            self.sheets_service.update_cell(self.sheet_name, row_index, 11, new_status)
            self.sheets_service.update_cell(self.sheet_name, row_index, 12, json.dumps(historial))
            
            return True
        except Exception as e:
            print(f"Error updating cita status: {e}")
            import traceback
            traceback.print_exc()
            return False
