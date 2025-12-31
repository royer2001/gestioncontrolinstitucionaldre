from services.google_sheets import GoogleSheetsService
import datetime
import uuid
import json

class LicenseService:
    _sheets_ready = False
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.sheet_name = 'licencias'
        self.employees_sheet = 'empleados_licencias'
        # NOTA: NO llamar _ensure_sheets_ready() aquí para evitar conexión en import

    def _ensure_sheets_ready(self):
        if LicenseService._sheets_ready:
            return
        # Employees sheet - tracks each employee's license quota
        employee_headers = [
            'id', 'dni', 'nombres', 'apellidos', 'cargo', 'area', 
            'dias_totales', 'dias_usados', 'created_at', 'updated_at'
        ]
        self.sheets_service.ensure_sheet_exists(self.employees_sheet, employee_headers)
        
        # Licenses sheet - individual license records
        license_headers = [
            'id', 'empleado_id', 'dni', 'tipo_licencia', 'motivo', 
            'fecha_inicio', 'fecha_fin', 'dias_solicitados', 'estado',
            'observaciones', 'created_at', 'created_by'
        ]
        self.sheets_service.ensure_sheet_exists(self.sheet_name, license_headers)
        LicenseService._sheets_ready = True

    # ============ EMPLOYEE METHODS ============
    
    def get_or_create_employee(self, dni, nombres, apellidos, cargo='', area=''):
        """Get existing employee or create new one with default 20 days quota"""
        self._ensure_sheets_ready()
        existing = self.get_employee_by_dni(dni)
        if existing:
            return existing
        
        employee_id = str(uuid.uuid4())
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        row_data = [
            employee_id,
            dni,
            nombres,
            apellidos,
            cargo,
            area,
            20,  # dias_totales - default quota
            0,   # dias_usados
            now,
            now
        ]
        self.sheets_service.append_row(self.employees_sheet, row_data)
        
        return {
            'id': employee_id,
            'dni': dni,
            'nombres': nombres,
            'apellidos': apellidos,
            'cargo': cargo,
            'area': area,
            'dias_totales': 20,
            'dias_usados': 0
        }

    def get_employee_by_dni(self, dni):
        """Find employee by DNI"""
        self._ensure_sheets_ready()
        try:
            records = self.sheets_service.get_all_records(self.employees_sheet)
            for r in records:
                if str(r.get('dni', '')) == str(dni):
                    return r
            return None
        except Exception as e:
            print(f"Error finding employee: {e}")
            return None

    def get_all_employees(self):
        """Get all employees with their license balance"""
        self._ensure_sheets_ready()
        try:
            records = self.sheets_service.get_all_records(self.employees_sheet)
            for r in records:
                r['dias_disponibles'] = int(r.get('dias_totales', 20)) - int(r.get('dias_usados', 0))
            return records
        except Exception as e:
            print(f"Error fetching employees: {e}")
            return []

    def update_employee_days(self, employee_id, days_to_add):
        """Update employee's used days"""
        try:
            row_index = self.sheets_service.find_row_index_by_value(
                self.employees_sheet, employee_id, col_index=1
            )
            if not row_index:
                return False
            
            current_row = self.sheets_service.get_row_by_index(self.employees_sheet, row_index)
            current_used = int(current_row[7]) if current_row and len(current_row) > 7 else 0
            new_used = current_used + days_to_add
            
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update dias_usados (col 8) and updated_at (col 10)
            self.sheets_service.update_cell(self.employees_sheet, row_index, 8, new_used)
            self.sheets_service.update_cell(self.employees_sheet, row_index, 10, now)
            
            return True
        except Exception as e:
            print(f"Error updating employee days: {e}")
            return False

    # ============ LICENSE METHODS ============

    def create_license(self, data, created_by='Sistema'):
        """Create a new license request"""
        license_id = str(uuid.uuid4())
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate days
        fecha_inicio = datetime.datetime.strptime(data.get('fecha_inicio'), '%Y-%m-%d')
        fecha_fin = datetime.datetime.strptime(data.get('fecha_fin'), '%Y-%m-%d')
        dias_solicitados = (fecha_fin - fecha_inicio).days + 1
        
        # Get or create employee
        employee = self.get_or_create_employee(
            data.get('dni'),
            data.get('nombres'),
            data.get('apellidos'),
            data.get('cargo', ''),
            data.get('area', '')
        )
        
        # Check available days
        dias_disponibles = int(employee.get('dias_totales', 20)) - int(employee.get('dias_usados', 0))
        if dias_solicitados > dias_disponibles:
            return None, f"Solo tiene {dias_disponibles} días disponibles, solicita {dias_solicitados}"
        
        row_data = [
            license_id,
            employee['id'],
            data.get('dni'),
            data.get('tipo_licencia'),
            data.get('motivo', ''),
            data.get('fecha_inicio'),
            data.get('fecha_fin'),
            dias_solicitados,
            'APROBADO',  # Default status
            data.get('observaciones', ''),
            now,
            created_by
        ]
        
        self.sheets_service.append_row(self.sheet_name, row_data)
        
        # Update employee's used days
        self.update_employee_days(employee['id'], dias_solicitados)
        
        return license_id, None

    def get_all_licenses(self):
        """Get all license records enriched with employee data"""
        try:
            records = self.sheets_service.get_all_records(self.sheet_name)
            
            # Obtener todos los empleados para enriquecer los datos
            employees = self.get_all_employees()
            
            # Crear mapa de DNI a datos del empleado
            employee_map = {}
            for emp in employees:
                dni = str(emp.get('dni', ''))
                if dni:
                    employee_map[dni] = {
                        'nombres': emp.get('nombres', ''),
                        'apellidos': emp.get('apellidos', ''),
                        'cargo': emp.get('cargo', ''),
                        'area': emp.get('area', '')
                    }
            
            # Enriquecer cada licencia con datos del empleado
            for record in records:
                dni = str(record.get('dni', ''))
                if dni in employee_map:
                    record['nombres'] = employee_map[dni]['nombres']
                    record['apellidos'] = employee_map[dni]['apellidos']
                    record['cargo'] = employee_map[dni]['cargo']
                    record['area'] = employee_map[dni]['area']
                else:
                    record['nombres'] = ''
                    record['apellidos'] = ''
                    record['cargo'] = ''
                    record['area'] = ''
            
            return sorted(records, key=lambda x: x.get('created_at', ''), reverse=True)
        except Exception as e:
            print(f"Error fetching licenses: {e}")
            return []

    def get_licenses_by_dni(self, dni):
        """Get all licenses for a specific employee"""
        try:
            all_licenses = self.get_all_licenses()
            return [l for l in all_licenses if str(l.get('dni', '')) == str(dni)]
        except Exception as e:
            print(f"Error fetching licenses by dni: {e}")
            return []

    def get_license_summary(self):
        """Get summary statistics"""
        try:
            employees = self.get_all_employees()
            licenses = self.get_all_licenses()
            
            current_year = datetime.datetime.now().year
            this_year_licenses = [l for l in licenses if l.get('fecha_inicio', '').startswith(str(current_year))]
            
            return {
                'total_empleados': len(employees),
                'total_licencias': len(licenses),
                'licencias_este_año': len(this_year_licenses),
                'empleados_sin_dias': len([e for e in employees if int(e.get('dias_disponibles', 0)) <= 0]),
                'por_tipo': {
                    'enfermedad': len([l for l in this_year_licenses if l.get('tipo_licencia') == 'Enfermedad']),
                    'maternidad': len([l for l in this_year_licenses if l.get('tipo_licencia') == 'Maternidad']),
                    'paternidad': len([l for l in this_year_licenses if l.get('tipo_licencia') == 'Paternidad']),
                    'personal': len([l for l in this_year_licenses if l.get('tipo_licencia') == 'Personal']),
                    'otros': len([l for l in this_year_licenses if l.get('tipo_licencia') == 'Otros'])
                }
            }
        except Exception as e:
            print(f"Error getting summary: {e}")
            return {}
