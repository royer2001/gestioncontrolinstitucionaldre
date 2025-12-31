from services.google_sheets import GoogleSheetsService
import datetime
import uuid
import json

class VehicleService:
    _sheets_ready = False
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.sheet_name = 'registros_vehiculares'
        self.inventory_sheet_name = 'inventario_vehiculos'
        self.maintenance_sheet_name = 'gastos_mantenimiento'
        self.handover_sheet_name = 'actas_entrega_recepcion'
        self.service_req_sheet_name = 'requerimientos_servicio'
        # NOTA: NO llamar _ensure_sheets_ready() aquí para evitar conexión en import

    def _ensure_sheets_ready(self):
        if VehicleService._sheets_ready:
            return
        # Commission Request Headers
        request_headers = [
            'id', 'dependencia', 'dia', 'hora', 'lugar', 'motivo', 'usuarios', 
            'placa', 'marca', 'chofer', 'hora_salida', 'hora_regreso', 'estado', 'created_at'
        ]
        self.sheets_service.ensure_sheet_exists(self.sheet_name, request_headers)

        # Vehicle Inventory Headers
        inventory_headers = [
            'id', 'tipo', 'marca', 'modelo', 'placa', 'anio', 'motor', 'chasis',
            'cilindros', 'asientos', 'color_asientos', 'estado', 'kilometraje',
            'combustible', 'fecha_soat', 'fecha_revision', 'observaciones', 'created_at'
        ]
        self.sheets_service.ensure_sheet_exists(self.inventory_sheet_name, inventory_headers)

        # Maintenance Expense Headers
        maintenance_headers = [
            'id', 'vehiculo_id', 'fecha', 'factura', 'kilometraje', 'orden_sc', 'factor_proveedor',
            'detalle', 'costo', 'vigilante', 'responsable', 'created_at'
        ]
        self.sheets_service.ensure_sheet_exists(self.maintenance_sheet_name, maintenance_headers)

        # Handover Headers
        handover_headers = [
           'id', 'fecha', 'entidad', 'denominacion', 'placa', 'color', 'kilometraje',
           'carroceria', 'n_motor', 'sistemas_json', 'abastecimiento', 'recepciona', 'created_at'
        ]
        self.sheets_service.ensure_sheet_exists(self.handover_sheet_name, handover_headers)

        # Service Requirement Headers
        service_req_headers = [
            'id', 'conductor', 'vehiculo_id', 'estado_vehiculo', 'estado_motor', 
            'encendido_electrico', 'transmision', 'pintura_carroceria', 'llantas',
            'herramientas', 'implementos_aseo', 'comisiones_realizadas', 'motivo', 'created_at'
        ]
        self.sheets_service.ensure_sheet_exists(self.service_req_sheet_name, service_req_headers)
        VehicleService._sheets_ready = True

    # --- Commission Requests Methods ---
    def create_request(self, data):
        self._ensure_sheets_ready()
        req_id = str(uuid.uuid4())
        row_data = [
            req_id,
            data.get('dependencia', ''),
            data.get('dia', ''),
            data.get('hora', ''),
            data.get('lugar', ''),
            data.get('motivo', ''),
            data.get('usuarios', ''),
            data.get('placa', ''),
            data.get('marca', ''),
            data.get('chofer', ''),
            data.get('hora_salida', ''),
            data.get('hora_regreso', ''),
            'PENDIENTE', 
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        self.sheets_service.append_row(self.sheet_name, row_data)
        return req_id

    def get_all_requests(self):
        self._ensure_sheets_ready()
        try:
            return self.sheets_service.get_all_records(self.sheet_name)
        except Exception as e:
            print(f"Error fetching vehicle requests: {e}")
            return []
    
    def update_request(self, req_id, data):
        try:
            row_index = self.sheets_service.find_row_index_by_value(self.sheet_name, req_id, col_index=1)
            if not row_index:
                return False
            
            mapping = {
                'dependencia': 2, 'dia': 3, 'hora': 4, 'lugar': 5, 'motivo': 6,
                'usuarios': 7, 'placa': 8, 'marca': 9, 'chofer': 10,
                'hora_salida': 11, 'hora_regreso': 12, 'estado': 13
            }
            
            for key, col_idx in mapping.items():
                if key in data:
                    self.sheets_service.update_cell(self.sheet_name, row_index, col_idx, data[key])
            return True
        except Exception as e:
            print(f"Error updating request: {e}")
            return False

    # --- Vehicle Inventory Methods ---
    def create_vehicle(self, data):
        veh_id = str(uuid.uuid4())
        row_data = [
            veh_id,
            data.get('tipo', ''),
            data.get('marca', ''),
            data.get('modelo', ''),
            data.get('placa', ''),
            data.get('anio', ''),
            data.get('motor', ''),
            data.get('chasis', ''),
            data.get('cilindros', ''),
            data.get('asientos', ''),
            data.get('color_asientos', ''),
            data.get('estado', 'Operativo'),
            data.get('kilometraje', ''),
            data.get('combustible', ''),
            data.get('fecha_soat', ''),
            data.get('fecha_revision', ''),
            data.get('observaciones', ''),
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        self.sheets_service.append_row(self.inventory_sheet_name, row_data)
        return veh_id

    def get_all_vehicles(self):
        try:
            return self.sheets_service.get_all_records(self.inventory_sheet_name)
        except Exception as e:
            print(f"Error fetching vehicles: {e}")
            return []

    def update_vehicle(self, veh_id, data):
        try:
            row_index = self.sheets_service.find_row_index_by_value(self.inventory_sheet_name, veh_id, col_index=1)
            if not row_index:
                return False

            mapping = {
                'tipo': 2, 'marca': 3, 'modelo': 4, 'placa': 5, 'anio': 6,
                'motor': 7, 'chasis': 8, 'cilindros': 9, 'asientos': 10,
                'color_asientos': 11, 'estado': 12, 'kilometraje': 13,
                'combustible': 14, 'fecha_soat': 15, 'fecha_revision': 16,
                'observaciones': 17
            }

            for key, col_idx in mapping.items():
                if key in data:
                    self.sheets_service.update_cell(self.inventory_sheet_name, row_index, col_idx, data[key])
            return True
        except Exception as e:
            print(f"Error updating vehicle: {e}")
            return False

    # --- Maintenance Expenses Methods ---
    def create_maintenance_expense(self, data):
        expense_id = str(uuid.uuid4())
        row_data = [
            expense_id,
            data.get('vehiculo_id', ''),
            data.get('fecha', ''),
            data.get('factura', ''),
            data.get('kilometraje', ''),
            data.get('orden_sc', ''),
            data.get('factor_proveedor', ''),
            data.get('detalle', ''),
            data.get('costo', ''),
            data.get('vigilante', ''),
            data.get('responsable', ''),
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        self.sheets_service.append_row(self.maintenance_sheet_name, row_data)
        return expense_id
    
    def get_all_maintenance_expenses(self):
        try:
            return self.sheets_service.get_all_records(self.maintenance_sheet_name)
        except Exception as e:
            print(f"Error fetching maintenance expenses: {e}")
            return []

    # --- Handover Methods ---
    def create_handover(self, data):
        handover_id = str(uuid.uuid4())
        # The 'sistemas' will be stored as a JSON string
        sistemas_json = json.dumps(data.get('sistemas', {}))

        row_data = [
            handover_id,
            data.get('fecha', ''),
            data.get('entidad', ''),
            data.get('denominacion', ''),
            data.get('placa', ''),
            data.get('color', ''),
            data.get('kilometraje', ''),
            data.get('carroceria', ''),
            data.get('n_motor', ''),
            sistemas_json,
            data.get('abastecimiento', ''),
            data.get('recepciona', ''),
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        self.sheets_service.append_row(self.handover_sheet_name, row_data)
        return handover_id

    def get_all_handovers(self):
        try:
            records = self.sheets_service.get_all_records(self.handover_sheet_name)
            # Parse the JSON string back to object
            for r in records:
                if 'sistemas_json' in r and r['sistemas_json']:
                    try:
                        r['sistemas'] = json.loads(r['sistemas_json'])
                    except:
                        r['sistemas'] = {}
            return records
        except Exception as e:
            print(f"Error fetching handovers: {e}")
            return []

    # --- Service Requirements Methods ---
    def create_service_requirement(self, data):
        req_id = str(uuid.uuid4())
        row_data = [
            req_id,
            data.get('conductor', ''),
            data.get('vehiculo_id', ''),
            data.get('estado_vehiculo', ''),
            data.get('estado_motor', ''),
            data.get('encendido_electrico', ''),
            data.get('transmision', ''),
            data.get('pintura_carroceria', ''),
            data.get('llantas', ''),
            data.get('herramientas', ''),
            data.get('implementos_aseo', ''),
            data.get('comisiones_realizadas', ''),
            data.get('motivo', ''),
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        self.sheets_service.append_row(self.service_req_sheet_name, row_data)
        return req_id

    def get_all_service_requirements(self):
        try:
            return self.sheets_service.get_all_records(self.service_req_sheet_name)
        except Exception as e:
            print(f"Error fetching service requirements: {e}")
            return []
