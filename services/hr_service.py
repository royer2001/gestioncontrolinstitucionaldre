from services.google_sheets import GoogleSheetsService
import datetime
import uuid

class HRService:
    _sheets_ready = False
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.employees_sheet = 'rrhh_personal'
        self.vacations_sheet = 'rrhh_vacaciones'
        self.activities_sheet = 'rrhh_actividades'
        # NOTA: NO llamar _ensure_sheets_ready() aquí para evitar conexión en import

    def _ensure_sheets_ready(self):
        if HRService._sheets_ready:
            return
        # Personal data sheet
        employee_headers = [
            'id', 'dni', 'nombres', 'apellidos', 'fecha_nacimiento', 'genero',
            'direccion', 'telefono', 'correo', 'cargo', 'area', 'fecha_ingreso',
            'tipo_contrato', 'estado', 'observaciones', 'created_at', 'updated_at'
        ]
        self.sheets_service.ensure_sheet_exists(self.employees_sheet, employee_headers)
        
        # Vacations sheet
        vacation_headers = [
            'id', 'empleado_id', 'dni', 'periodo', 'fecha_inicio', 'fecha_fin',
            'dias_tomados', 'dias_pendientes', 'estado', 'observaciones', 'created_at'
        ]
        self.sheets_service.ensure_sheet_exists(self.vacations_sheet, vacation_headers)
        
        # HR Activities sheet
        activity_headers = [
            'id', 'empleado_id', 'dni', 'tipo_actividad', 'descripcion',
            'fecha', 'documento_referencia', 'estado', 'created_at', 'created_by'
        ]
        self.sheets_service.ensure_sheet_exists(self.activities_sheet, activity_headers)
        HRService._sheets_ready = True

    # ============ EMPLOYEE METHODS ============
    
    def create_employee(self, data):
        """Create a new employee record"""
        self._ensure_sheets_ready()
        employee_id = str(uuid.uuid4())
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        row_data = [
            employee_id,
            data.get('dni', ''),
            data.get('nombres', ''),
            data.get('apellidos', ''),
            data.get('fecha_nacimiento', ''),
            data.get('genero', ''),
            data.get('direccion', ''),
            data.get('telefono', ''),
            data.get('correo', ''),
            data.get('cargo', ''),
            data.get('area', ''),
            data.get('fecha_ingreso', ''),
            data.get('tipo_contrato', 'Nombrado'),
            'ACTIVO',
            data.get('observaciones', ''),
            now,
            now
        ]
        self.sheets_service.append_row(self.employees_sheet, row_data)
        return employee_id

    def get_all_employees(self):
        """Get all employees"""
        self._ensure_sheets_ready()
        try:
            records = self.sheets_service.get_all_records(self.employees_sheet)
            return sorted(records, key=lambda x: x.get('apellidos', ''))
        except Exception as e:
            print(f"Error fetching employees: {e}")
            return []

    def get_employee_by_id(self, employee_id):
        """Get employee by ID"""
        try:
            records = self.sheets_service.get_all_records(self.employees_sheet)
            for r in records:
                if r.get('id') == employee_id:
                    return r
            return None
        except:
            return None

    def get_employee_by_dni(self, dni):
        """Get employee by DNI"""
        try:
            records = self.sheets_service.get_all_records(self.employees_sheet)
            for r in records:
                if str(r.get('dni', '')) == str(dni):
                    return r
            return None
        except:
            return None

    def update_employee(self, employee_id, data):
        """Update employee data"""
        try:
            row_index = self.sheets_service.find_row_index_by_value(
                self.employees_sheet, employee_id, col_index=1
            )
            if not row_index:
                return False
            
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update fields (skip id, created_at)
            updates = {
                2: data.get('dni'),
                3: data.get('nombres'),
                4: data.get('apellidos'),
                5: data.get('fecha_nacimiento'),
                6: data.get('genero'),
                7: data.get('direccion'),
                8: data.get('telefono'),
                9: data.get('correo'),
                10: data.get('cargo'),
                11: data.get('area'),
                12: data.get('fecha_ingreso'),
                13: data.get('tipo_contrato'),
                14: data.get('estado'),
                15: data.get('observaciones'),
                17: now  # updated_at
            }
            
            for col, value in updates.items():
                if value is not None:
                    self.sheets_service.update_cell(self.employees_sheet, row_index, col, value)
            
            return True
        except Exception as e:
            print(f"Error updating employee: {e}")
            return False

    # ============ VACATION METHODS ============
    
    def create_vacation(self, data):
        """Register a vacation period"""
        vacation_id = str(uuid.uuid4())
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate days
        fecha_inicio = datetime.datetime.strptime(data.get('fecha_inicio'), '%Y-%m-%d')
        fecha_fin = datetime.datetime.strptime(data.get('fecha_fin'), '%Y-%m-%d')
        dias_tomados = (fecha_fin - fecha_inicio).days + 1
        
        row_data = [
            vacation_id,
            data.get('empleado_id', ''),
            data.get('dni', ''),
            data.get('periodo', str(datetime.datetime.now().year)),
            data.get('fecha_inicio'),
            data.get('fecha_fin'),
            dias_tomados,
            data.get('dias_pendientes', 30 - dias_tomados),
            data.get('estado', 'PROGRAMADO'),
            data.get('observaciones', ''),
            now
        ]
        self.sheets_service.append_row(self.vacations_sheet, row_data)
        return vacation_id

    def get_all_vacations(self):
        """Get all vacation records"""
        try:
            records = self.sheets_service.get_all_records(self.vacations_sheet)
            return sorted(records, key=lambda x: x.get('fecha_inicio', ''), reverse=True)
        except Exception as e:
            print(f"Error fetching vacations: {e}")
            return []

    def get_vacations_by_employee(self, empleado_id):
        """Get vacations for a specific employee"""
        try:
            all_vacations = self.get_all_vacations()
            return [v for v in all_vacations if v.get('empleado_id') == empleado_id]
        except:
            return []

    # ============ ACTIVITY METHODS ============
    
    def create_activity(self, data, created_by='Sistema'):
        """Register an HR activity"""
        activity_id = str(uuid.uuid4())
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        row_data = [
            activity_id,
            data.get('empleado_id', ''),
            data.get('dni', ''),
            data.get('tipo_actividad', ''),
            data.get('descripcion', ''),
            data.get('fecha', now[:10]),
            data.get('documento_referencia', ''),
            data.get('estado', 'REGISTRADO'),
            now,
            created_by
        ]
        self.sheets_service.append_row(self.activities_sheet, row_data)
        return activity_id

    def get_all_activities(self):
        """Get all HR activities"""
        try:
            records = self.sheets_service.get_all_records(self.activities_sheet)
            return sorted(records, key=lambda x: x.get('created_at', ''), reverse=True)
        except Exception as e:
            print(f"Error fetching activities: {e}")
            return []

    # ============ SUMMARY ============
    
    def get_summary(self):
        """Get HR summary statistics"""
        try:
            employees = self.get_all_employees()
            vacations = self.get_all_vacations()
            activities = self.get_all_activities()
            
            current_year = datetime.datetime.now().year
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            
            # Employees on vacation now
            on_vacation = [v for v in vacations 
                          if v.get('fecha_inicio', '') <= today <= v.get('fecha_fin', '')]
            
            return {
                'total_empleados': len(employees),
                'empleados_activos': len([e for e in employees if e.get('estado') == 'ACTIVO']),
                'empleados_inactivos': len([e for e in employees if e.get('estado') != 'ACTIVO']),
                'en_vacaciones': len(on_vacation),
                'vacaciones_programadas': len([v for v in vacations if v.get('estado') == 'PROGRAMADO']),
                'actividades_mes': len([a for a in activities if a.get('created_at', '').startswith(f'{current_year}-{datetime.datetime.now().month:02d}')]),
                'por_area': self._count_by_field(employees, 'area'),
                'por_tipo_contrato': self._count_by_field(employees, 'tipo_contrato')
            }
        except Exception as e:
            print(f"Error getting summary: {e}")
            return {}

    def _count_by_field(self, records, field):
        counts = {}
        for r in records:
            value = r.get(field, 'Sin especificar') or 'Sin especificar'
            counts[value] = counts.get(value, 0) + 1
        return counts
