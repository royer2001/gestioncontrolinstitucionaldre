from services.google_sheets import GoogleSheetsService
import datetime
import uuid

class TurnService:
    _sheets_ready = False
    
    # Áreas de la DRE
    AREAS = {
        'DGI': {'nombre': 'Dirección de Gestión Institucional', 'prefijo': 'A'},
        'DGP': {'nombre': 'Dirección de Gestión Pedagógica', 'prefijo': 'B'},
        'TRAMITE': {'nombre': 'Trámite Documentario', 'prefijo': 'C'},
        'ACTAS': {'nombre': 'Actas y Certificados', 'prefijo': 'D'},
        'TESORERIA': {'nombre': 'Tesorería', 'prefijo': 'E'},
        'ESCALAFON': {'nombre': 'Escalafón', 'prefijo': 'F'},
        'RRHH': {'nombre': 'Recursos Humanos', 'prefijo': 'G'},
        'OCI': {'nombre': 'Órgano de Control Institucional', 'prefijo': 'H'},
        'DIRECCION': {'nombre': 'Dirección Regional', 'prefijo': 'I'},
        'LEGAL': {'nombre': 'Asesoría Legal', 'prefijo': 'J'},
    }
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.turns_sheet = 'turnos'
        self.turn_config_sheet = 'turnos_config'
    
    def _ensure_sheets_ready(self):
        if TurnService._sheets_ready:
            return
        
        # Turns sheet headers
        turn_headers = [
            'id', 'numero_turno', 'codigo_area', 'nombre_area', 'dni_usuario',
            'nombre_usuario', 'motivo', 'estado', 'fecha_creacion', 'hora_creacion',
            'fecha_llamado', 'hora_llamado', 'fecha_atencion', 'hora_atencion',
            'ventanilla', 'tiempo_espera_minutos', 'creado_por', 'atendido_por'
        ]
        self.sheets_service.ensure_sheet_exists(self.turns_sheet, turn_headers)
        
        # Config sheet for turn counters per day
        config_headers = [
            'fecha', 'codigo_area', 'ultimo_numero', 'actualizado_at'
        ]
        self.sheets_service.ensure_sheet_exists(self.turn_config_sheet, config_headers)
        
        TurnService._sheets_ready = True
    
    def get_areas(self):
        """Obtener todas las áreas disponibles"""
        return [
            {'codigo': codigo, 'nombre': info['nombre'], 'prefijo': info['prefijo']}
            for codigo, info in self.AREAS.items()
        ]
    
    def _get_next_turn_number(self, codigo_area):
        """Obtener el siguiente número de turno para un área en el día actual"""
        self._ensure_sheets_ready()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        try:
            records = self.sheets_service.get_all_records(self.turn_config_sheet)
            
            # Buscar la configuración para hoy y esta área
            for idx, record in enumerate(records):
                if record.get('fecha') == today and record.get('codigo_area') == codigo_area:
                    ultimo = int(record.get('ultimo_numero', 0))
                    nuevo_numero = ultimo + 1
                    
                    # Actualizar el contador
                    row_index = idx + 2  # +2 porque hay header y es 1-based
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.sheets_service.update_cell(self.turn_config_sheet, row_index, 3, nuevo_numero)
                    self.sheets_service.update_cell(self.turn_config_sheet, row_index, 4, now)
                    
                    return nuevo_numero
            
            # No existe para hoy, crear nuevo registro
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.sheets_service.append_row(self.turn_config_sheet, [today, codigo_area, 1, now])
            return 1
            
        except Exception as e:
            print(f"Error getting next turn number: {e}")
            return 1
    
    def create_turn(self, data, created_by='TOTEM'):
        """Crear un nuevo turno"""
        self._ensure_sheets_ready()
        
        codigo_area = data.get('codigo_area')
        if codigo_area not in self.AREAS:
            return None, "Área no válida"
        
        area_info = self.AREAS[codigo_area]
        turn_number = self._get_next_turn_number(codigo_area)
        
        # Formato: PREFIJO + número con padding (ej: A001, B015)
        numero_turno = f"{area_info['prefijo']}{turn_number:03d}"
        
        turn_id = str(uuid.uuid4())
        now = datetime.datetime.now()
        fecha = now.strftime('%Y-%m-%d')
        hora = now.strftime('%H:%M:%S')
        
        row_data = [
            turn_id,
            numero_turno,
            codigo_area,
            area_info['nombre'],
            data.get('dni_usuario', ''),
            data.get('nombre_usuario', 'Ciudadano'),
            data.get('motivo', ''),
            'EN_ESPERA',  # Estado inicial
            fecha,
            hora,
            '',  # fecha_llamado
            '',  # hora_llamado
            '',  # fecha_atencion
            '',  # hora_atencion
            '',  # ventanilla
            '',  # tiempo_espera_minutos
            created_by,
            ''   # atendido_por
        ]
        
        self.sheets_service.append_row(self.turns_sheet, row_data)
        
        return {
            'id': turn_id,
            'numero_turno': numero_turno,
            'codigo_area': codigo_area,
            'nombre_area': area_info['nombre'],
            'fecha': fecha,
            'hora': hora,
            'estado': 'EN_ESPERA',
            'posicion_cola': self._get_queue_position(codigo_area, numero_turno)
        }, None
    
    def _get_queue_position(self, codigo_area, numero_turno):
        """Obtener la posición en la cola para un turno"""
        try:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            records = self.sheets_service.get_all_records(self.turns_sheet)
            
            waiting_turns = [
                r for r in records
                if r.get('codigo_area') == codigo_area
                and r.get('estado') == 'EN_ESPERA'
                and r.get('fecha_creacion') == today
            ]
            
            # Ordenar por hora de creación
            waiting_turns.sort(key=lambda x: x.get('hora_creacion', ''))
            
            for idx, turn in enumerate(waiting_turns):
                if turn.get('numero_turno') == numero_turno:
                    return idx + 1
            
            return len(waiting_turns) + 1
        except:
            return 1
    
    def get_waiting_turns_today(self, codigo_area=None):
        """Obtener turnos en espera del día actual"""
        self._ensure_sheets_ready()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        try:
            records = self.sheets_service.get_all_records(self.turns_sheet)
            
            waiting_turns = [
                r for r in records
                if r.get('estado') == 'EN_ESPERA'
                and r.get('fecha_creacion') == today
            ]
            
            if codigo_area:
                waiting_turns = [t for t in waiting_turns if t.get('codigo_area') == codigo_area]
            
            waiting_turns.sort(key=lambda x: (x.get('hora_creacion', ''), x.get('numero_turno', '')))
            
            return waiting_turns
        except Exception as e:
            print(f"Error fetching waiting turns: {e}")
            return []
    
    def get_current_turns(self):
        """Obtener los turnos que están siendo atendidos actualmente"""
        self._ensure_sheets_ready()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        try:
            records = self.sheets_service.get_all_records(self.turns_sheet)
            
            current_turns = [
                r for r in records
                if r.get('estado') == 'LLAMANDO'
                and r.get('fecha_creacion') == today
            ]
            
            return current_turns
        except Exception as e:
            print(f"Error fetching current turns: {e}")
            return []
    
    def get_turns_by_date(self, fecha=None):
        """Obtener todos los turnos de una fecha"""
        self._ensure_sheets_ready()
        if not fecha:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d')
        
        try:
            records = self.sheets_service.get_all_records(self.turns_sheet)
            turns = [r for r in records if r.get('fecha_creacion') == fecha]
            turns.sort(key=lambda x: (x.get('hora_creacion', ''), x.get('numero_turno', '')))
            return turns
        except Exception as e:
            print(f"Error fetching turns by date: {e}")
            return []
    
    def call_next_turn(self, codigo_area, ventanilla='1', user='Sistema'):
        """Llamar al siguiente turno en cola de un área"""
        self._ensure_sheets_ready()
        
        waiting_turns = self.get_waiting_turns_today(codigo_area)
        
        if not waiting_turns:
            return None, "No hay turnos en espera para esta área"
        
        next_turn = waiting_turns[0]
        turn_id = next_turn.get('id')
        
        # Buscar la fila y actualizar
        try:
            row_index = self.sheets_service.find_row_index_by_value(self.turns_sheet, turn_id, col_index=1)
            if not row_index:
                return None, "No se encontró el turno"
            
            now = datetime.datetime.now()
            fecha_llamado = now.strftime('%Y-%m-%d')
            hora_llamado = now.strftime('%H:%M:%S')
            
            # Calcular tiempo de espera
            hora_creacion = datetime.datetime.strptime(
                f"{next_turn.get('fecha_creacion')} {next_turn.get('hora_creacion')}",
                '%Y-%m-%d %H:%M:%S'
            )
            tiempo_espera = int((now - hora_creacion).total_seconds() / 60)
            
            # Actualizar estado a LLAMANDO
            self.sheets_service.update_cell(self.turns_sheet, row_index, 8, 'LLAMANDO')
            self.sheets_service.update_cell(self.turns_sheet, row_index, 11, fecha_llamado)
            self.sheets_service.update_cell(self.turns_sheet, row_index, 12, hora_llamado)
            self.sheets_service.update_cell(self.turns_sheet, row_index, 15, ventanilla)
            self.sheets_service.update_cell(self.turns_sheet, row_index, 16, tiempo_espera)
            self.sheets_service.update_cell(self.turns_sheet, row_index, 18, user)
            
            return {
                'id': turn_id,
                'numero_turno': next_turn.get('numero_turno'),
                'codigo_area': codigo_area,
                'nombre_area': next_turn.get('nombre_area'),
                'ventanilla': ventanilla,
                'nombre_usuario': next_turn.get('nombre_usuario'),
                'tiempo_espera': tiempo_espera
            }, None
            
        except Exception as e:
            print(f"Error calling next turn: {e}")
            return None, str(e)
    
    def complete_turn(self, turn_id, user='Sistema'):
        """Marcar un turno como atendido"""
        self._ensure_sheets_ready()
        
        try:
            row_index = self.sheets_service.find_row_index_by_value(self.turns_sheet, turn_id, col_index=1)
            if not row_index:
                return False, "No se encontró el turno"
            
            now = datetime.datetime.now()
            fecha_atencion = now.strftime('%Y-%m-%d')
            hora_atencion = now.strftime('%H:%M:%S')
            
            self.sheets_service.update_cell(self.turns_sheet, row_index, 8, 'ATENDIDO')
            self.sheets_service.update_cell(self.turns_sheet, row_index, 13, fecha_atencion)
            self.sheets_service.update_cell(self.turns_sheet, row_index, 14, hora_atencion)
            
            return True, None
            
        except Exception as e:
            print(f"Error completing turn: {e}")
            return False, str(e)
    
    def cancel_turn(self, turn_id, user='Sistema'):
        """Cancelar/No se presentó un turno"""
        self._ensure_sheets_ready()
        
        try:
            row_index = self.sheets_service.find_row_index_by_value(self.turns_sheet, turn_id, col_index=1)
            if not row_index:
                return False, "No se encontró el turno"
            
            self.sheets_service.update_cell(self.turns_sheet, row_index, 8, 'CANCELADO')
            
            return True, None
            
        except Exception as e:
            print(f"Error canceling turn: {e}")
            return False, str(e)
    
    def get_statistics(self, fecha=None):
        """Obtener estadísticas de turnos"""
        if not fecha:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d')
        
        turns = self.get_turns_by_date(fecha)
        
        total = len(turns)
        en_espera = len([t for t in turns if t.get('estado') == 'EN_ESPERA'])
        llamando = len([t for t in turns if t.get('estado') == 'LLAMANDO'])
        atendidos = len([t for t in turns if t.get('estado') == 'ATENDIDO'])
        cancelados = len([t for t in turns if t.get('estado') == 'CANCELADO'])
        
        # Tiempo promedio de espera
        tiempos = [int(t.get('tiempo_espera_minutos', 0)) for t in turns if t.get('tiempo_espera_minutos')]
        tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
        
        # Por área
        por_area = {}
        for t in turns:
            area = t.get('codigo_area', 'OTRO')
            if area not in por_area:
                por_area[area] = {'total': 0, 'atendidos': 0, 'en_espera': 0}
            por_area[area]['total'] += 1
            if t.get('estado') == 'ATENDIDO':
                por_area[area]['atendidos'] += 1
            elif t.get('estado') == 'EN_ESPERA':
                por_area[area]['en_espera'] += 1
        
        return {
            'fecha': fecha,
            'total': total,
            'en_espera': en_espera,
            'llamando': llamando,
            'atendidos': atendidos,
            'cancelados': cancelados,
            'tiempo_promedio_espera': round(tiempo_promedio, 1),
            'por_area': por_area
        }
