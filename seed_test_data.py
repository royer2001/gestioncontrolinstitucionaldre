"""
Script para generar datos de prueba para el sistema de control DRE.
Incluye:
- Hoja de ROLES con permisos (tabla maestra)
- Usuarios con rol_id como llave foránea
- Personal de RRHH
- Citas de prueba

Diseño relacional:
- roles: tabla maestra de roles con permisos
- usuarios: referencia a roles mediante rol_id (FK)
"""
import hashlib
from services.google_sheets import GoogleSheetsService
import datetime
import uuid
import time

def hash_password(password):
    """Genera hash SHA256 de la contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_roles_table():
    """
    Crea la tabla maestra de roles con permisos.
    Esta tabla sirve como referencia para los usuarios (diseño relacional).
    """
    import json
    service = GoogleSheetsService()
    
    # Headers para la hoja de roles
    role_headers = [
        'rol_id',           # ID único del rol (PK)
        'codigo',           # Código corto del rol
        'nombre',           # Nombre descriptivo
        'descripcion',      # Descripción del rol
        'nivel_acceso',     # Nivel de acceso (1-10)
        'permisos_json',    # Permisos en formato JSON
        'activo',           # Si el rol está activo
        'created_at',
        'updated_at'
    ]
    
    service.ensure_sheet_exists('roles', role_headers)
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Definición de roles del sistema con sus permisos
    roles = [
        {
            'rol_id': 'ROL001',
            'codigo': 'admin',
            'nombre': 'Administrador del Sistema',
            'descripcion': 'Acceso completo a todas las funcionalidades del sistema',
            'nivel_acceso': 10,
            'permisos': {
                'usuarios': ['crear', 'leer', 'editar', 'eliminar'],
                'roles': ['crear', 'leer', 'editar', 'eliminar'],
                'personal': ['crear', 'leer', 'editar', 'eliminar'],
                'citas': ['crear', 'leer', 'editar', 'eliminar', 'aprobar', 'rechazar'],
                'ocurrencias': ['crear', 'leer', 'editar', 'eliminar', 'aprobar'],
                'visitas': ['crear', 'leer', 'editar', 'eliminar'],
                'vehiculos': ['crear', 'leer', 'editar', 'eliminar'],
                'patrimonio': ['crear', 'leer', 'editar', 'eliminar'],
                'licencias': ['crear', 'leer', 'editar', 'eliminar', 'aprobar'],
                'reportes': ['ver', 'exportar'],
                'configuracion': ['leer', 'editar']
            }
        },
        {
            'rol_id': 'ROL002',
            'codigo': 'director',
            'nombre': 'Director Regional',
            'descripcion': 'Máxima autoridad de la DRE, acceso a reportes y aprobaciones',
            'nivel_acceso': 9,
            'permisos': {
                'personal': ['leer'],
                'citas': ['leer', 'aprobar', 'rechazar'],
                'ocurrencias': ['leer', 'aprobar'],
                'visitas': ['leer'],
                'vehiculos': ['leer'],
                'patrimonio': ['leer'],
                'licencias': ['leer', 'aprobar'],
                'reportes': ['ver', 'exportar']
            }
        },
        {
            'rol_id': 'ROL003',
            'codigo': 'subdirector',
            'nombre': 'Subdirector',
            'descripcion': 'Segunda autoridad, apoyo en gestión y supervisión',
            'nivel_acceso': 8,
            'permisos': {
                'personal': ['leer'],
                'citas': ['leer', 'aprobar', 'rechazar'],
                'ocurrencias': ['leer'],
                'visitas': ['leer'],
                'vehiculos': ['leer'],
                'patrimonio': ['leer'],
                'licencias': ['leer'],
                'reportes': ['ver', 'exportar']
            }
        },
        {
            'rol_id': 'ROL004',
            'codigo': 'jefe_rrhh',
            'nombre': 'Jefe de Recursos Humanos',
            'descripcion': 'Gestión integral del personal y licencias',
            'nivel_acceso': 7,
            'permisos': {
                'personal': ['crear', 'leer', 'editar', 'eliminar'],
                'licencias': ['crear', 'leer', 'editar', 'eliminar', 'aprobar'],
                'citas': ['leer'],
                'reportes': ['ver', 'exportar']
            }
        },
        {
            'rol_id': 'ROL005',
            'codigo': 'jefe_bienestar',
            'nombre': 'Jefe de Bienestar Social',
            'descripcion': 'Gestión de bienestar del personal y atención social',
            'nivel_acceso': 6,
            'permisos': {
                'personal': ['leer'],
                'citas': ['leer', 'aprobar', 'rechazar'],
                'licencias': ['leer'],
                'reportes': ['ver']
            }
        },
        {
            'rol_id': 'ROL006',
            'codigo': 'coordinador_vigilante',
            'nombre': 'Coordinador de Vigilancia',
            'descripcion': 'Supervisión del equipo de vigilancia y gestión de turnos',
            'nivel_acceso': 5,
            'permisos': {
                'ocurrencias': ['crear', 'leer', 'editar'],
                'visitas': ['crear', 'leer', 'editar'],
                'vehiculos': ['leer'],
                'personal': ['leer'],
                'reportes': ['ver']
            }
        },
        {
            'rol_id': 'ROL007',
            'codigo': 'vigilante',
            'nombre': 'Vigilante',
            'descripcion': 'Registro de ocurrencias, visitas y control de accesos',
            'nivel_acceso': 3,
            'permisos': {
                'ocurrencias': ['crear', 'leer'],
                'visitas': ['crear', 'leer', 'editar'],
                'vehiculos': ['crear', 'leer']
            }
        },
        {
            'rol_id': 'ROL008',
            'codigo': 'secretario',
            'nombre': 'Secretario/Gestor de Citas',
            'descripcion': 'Gestión de citas y atención al público',
            'nivel_acceso': 4,
            'permisos': {
                'citas': ['crear', 'leer', 'editar', 'aprobar', 'rechazar'],
                'visitas': ['leer']
            }
        },
        {
            'rol_id': 'ROL009',
            'codigo': 'jefe_patrimonio',
            'nombre': 'Jefe de Patrimonio',
            'descripcion': 'Gestión de bienes patrimoniales e inventario',
            'nivel_acceso': 6,
            'permisos': {
                'patrimonio': ['crear', 'leer', 'editar', 'eliminar'],
                'reportes': ['ver', 'exportar']
            }
        },
        {
            'rol_id': 'ROL010',
            'codigo': 'jefe_abastecimiento',
            'nombre': 'Jefe de Abastecimiento',
            'descripcion': 'Gestión de compras y suministros',
            'nivel_acceso': 6,
            'permisos': {
                'patrimonio': ['leer'],
                'reportes': ['ver', 'exportar']
            }
        },
        {
            'rol_id': 'ROL011',
            'codigo': 'jefe_oci',
            'nombre': 'Jefe del Órgano de Control Institucional',
            'descripcion': 'Control interno y auditoría',
            'nivel_acceso': 8,
            'permisos': {
                'personal': ['leer'],
                'citas': ['leer'],
                'ocurrencias': ['leer'],
                'visitas': ['leer'],
                'vehiculos': ['leer'],
                'patrimonio': ['leer'],
                'licencias': ['leer'],
                'reportes': ['ver', 'exportar']
            }
        },
        {
            'rol_id': 'ROL012',
            'codigo': 'tecnico_patrimonio',
            'nombre': 'Técnico en Patrimonio',
            'descripcion': 'Soporte en gestión de bienes patrimoniales',
            'nivel_acceso': 4,
            'permisos': {
                'patrimonio': ['crear', 'leer', 'editar']
            }
        },
        {
            'rol_id': 'ROL013',
            'codigo': 'especialista_rrhh',
            'nombre': 'Especialista en RRHH',
            'descripcion': 'Soporte en gestión de personal y planillas',
            'nivel_acceso': 5,
            'permisos': {
                'personal': ['crear', 'leer', 'editar'],
                'licencias': ['crear', 'leer', 'editar']
            }
        },
        {
            'rol_id': 'ROL014',
            'codigo': 'auditor',
            'nombre': 'Auditor',
            'descripcion': 'Auditoría y control interno',
            'nivel_acceso': 6,
            'permisos': {
                'personal': ['leer'],
                'ocurrencias': ['leer'],
                'patrimonio': ['leer'],
                'reportes': ['ver']
            }
        },
        {
            'rol_id': 'ROL015',
            'codigo': 'recepcionista',
            'nombre': 'Recepcionista',
            'descripcion': 'Atención al público y registro de visitas',
            'nivel_acceso': 2,
            'permisos': {
                'citas': ['leer'],
                'visitas': ['crear', 'leer']
            }
        },
    ]
    
    sheet_name = 'roles'
    existing_records = service.get_all_records(sheet_name)
    existing_ids = {str(r.get('rol_id', '')) for r in existing_records}
    
    created_count = 0
    skipped_count = 0
    
    for rol in roles:
        if rol['rol_id'] in existing_ids:
            print(f"⏭️  Rol '{rol['nombre']}' (ID: {rol['rol_id']}) ya existe. Omitiendo...")
            skipped_count += 1
            continue
        
        row_data = [
            rol['rol_id'],
            rol['codigo'],
            rol['nombre'],
            rol['descripcion'],
            rol['nivel_acceso'],
            json.dumps(rol['permisos']),
            'SI',
            now,
            now
        ]
        
        service.append_row(sheet_name, row_data)
        print(f"✅ Rol creado: {rol['nombre']} (ID: {rol['rol_id']}, Nivel: {rol['nivel_acceso']})")
        created_count += 1
        time.sleep(0.5)  # Evitar límite de cuota
    
    print(f"\n📊 Resumen: {created_count} roles creados, {skipped_count} omitidos")
    
    # Retornar mapeo de código a rol_id para usarlo en usuarios
    return {rol['codigo']: rol['rol_id'] for rol in roles}


def create_test_users(role_mapping=None):
    """
    Crea usuarios de prueba con diferentes roles.
    Solo guarda rol_id como llave foránea - el resto de info del rol se obtiene de la tabla roles.
    """
    service = GoogleSheetsService()
    
    # Si no se proporciona mapeo, crear uno por defecto
    if role_mapping is None:
        role_mapping = {
            'admin': 'ROL001',
            'director': 'ROL002',
            'subdirector': 'ROL003',
            'jefe_rrhh': 'ROL004',
            'jefe_bienestar': 'ROL005',
            'coordinador_vigilante': 'ROL006',
            'vigilante': 'ROL007',
            'secretario': 'ROL008',
            'jefe_patrimonio': 'ROL009',
            'jefe_abastecimiento': 'ROL010',
            'jefe_oci': 'ROL011',
            'tecnico_patrimonio': 'ROL012',
            'especialista_rrhh': 'ROL013',
            'auditor': 'ROL014',
            'recepcionista': 'ROL015',
        }
    
    # Headers para la hoja de usuarios (diseño relacional limpio)
    # El rol_id es la ÚNICA referencia al rol - para obtener nombre, permisos, etc.
    # se debe hacer un JOIN/lookup con la tabla 'roles'
    user_headers = [
        'id',               # ID único del usuario (PK)
        'titulo',           # Título profesional (Dr., Ing., Lic., etc.) - puede ser vacío
        'nombre',           # Nombre completo (sin título)
        'dni',              # DNI como identificador de login
        'contraseña_hash',  # Hash de la contraseña
        'rol_id',           # Llave foránea a la tabla roles (FK -> roles.rol_id)
        'activo',           # Si el usuario está activo (SI/NO)
        'ultimo_acceso',    # Último acceso al sistema
        'created_at',
        'updated_at'
    ]
    
    service.ensure_sheet_exists('usuarios', user_headers)
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    # Lista de usuarios de prueba con diferentes roles
    test_users = [
        # Vigilantes
        {
            'titulo': '',
            'nombre': 'Juan Carlos Pérez García',
            'dni': '12345671',
            'password': 'vigilante123',
            'rol_codigo': 'vigilante'
        },
        {
            'titulo': '',
            'nombre': 'Miguel Ángel López Torres',
            'dni': '12345672',
            'password': 'vigilante123',
            'rol_codigo': 'vigilante'
        },
        {
            'titulo': '',
            'nombre': 'Roberto Sánchez Medina',
            'dni': '12345673',
            'password': 'vigilante123',
            'rol_codigo': 'vigilante'
        },
        # Coordinador de Vigilantes
        {
            'titulo': '',
            'nombre': 'Fernando José Ramírez Castro',
            'dni': '12345674',
            'password': 'coordinador123',
            'rol_codigo': 'coordinador_vigilante'
        },
        # Jefe de RRHH
        {
            'titulo': 'Lic.',
            'nombre': 'María Elena Vargas Rojas',
            'dni': '12345675',
            'password': 'rrhh123',
            'rol_codigo': 'jefe_rrhh'
        },
        # Jefe de Bienestar Social
        {
            'titulo': 'Lic.',
            'nombre': 'Carmen Rosa Díaz Mendoza',
            'dni': '12345676',
            'password': 'bienestar123',
            'rol_codigo': 'jefe_bienestar'
        },
        # Secretarios (Gestores de Citas)
        {
            'titulo': '',
            'nombre': 'Patricia Luz Fernández Quispe',
            'dni': '12345677',
            'password': 'secretaria123',
            'rol_codigo': 'secretario'
        },
        {
            'titulo': '',
            'nombre': 'Rosa María Huamán Chávez',
            'dni': '12345678',
            'password': 'secretaria123',
            'rol_codigo': 'secretario'
        },
        {
            'titulo': '',
            'nombre': 'Ana Lucía Paredes Valverde',
            'dni': '12345679',
            'password': 'secretaria123',
            'rol_codigo': 'secretario'
        },
        # Director
        {
            'titulo': 'Dr.',
            'nombre': 'Luis Alberto Morales Ramos',
            'dni': '12345680',
            'password': 'director123',
            'rol_codigo': 'director'
        },
        # Subdirector
        {
            'titulo': 'Ing.',
            'nombre': 'Carlos Eduardo Vega Salazar',
            'dni': '12345681',
            'password': 'subdirector123',
            'rol_codigo': 'subdirector'
        },
        # Jefe de Patrimonio
        {
            'titulo': 'CPC.',
            'nombre': 'Jorge Antonio Silva Mendoza',
            'dni': '12345682',
            'password': 'patrimonio123',
            'rol_codigo': 'jefe_patrimonio'
        },
        # Jefe de Abastecimiento
        {
            'titulo': 'Lic.',
            'nombre': 'Pedro Pablo Romero Flores',
            'dni': '12345683',
            'password': 'abastecimiento123',
            'rol_codigo': 'jefe_abastecimiento'
        },
        # Jefe de OCI (Órgano de Control Institucional)
        {
            'titulo': 'Dra.',
            'nombre': 'Silvia Elena Torres Acuña',
            'dni': '12345684',
            'password': 'oci123',
            'rol_codigo': 'jefe_oci'
        },
    ]
    
    sheet_name = 'usuarios'
    existing_records = service.get_all_records(sheet_name)
    existing_dnis = {str(r.get('dni', '')) for r in existing_records}
    
    created_count = 0
    skipped_count = 0
    
    for user in test_users:
        if user['dni'] in existing_dnis:
            print(f"⏭️  Usuario '{user['nombre']}' (DNI: {user['dni']}) ya existe. Omitiendo...")
            skipped_count += 1
            continue
        
        new_id = str(uuid.uuid4())
        password_hash = hash_password(user['password'])
        rol_codigo = user['rol_codigo']
        rol_id = role_mapping.get(rol_codigo, 'ROL007')  # Default a vigilante
        titulo = user.get('titulo', '')
        
        # Solo guardamos rol_id como FK - sin duplicar datos de la tabla roles
        user_data = [
            new_id,
            titulo,           # Título profesional (Dr., Ing., Lic., etc.)
            user['nombre'],
            user['dni'],
            password_hash,
            rol_id,           # FK a la tabla roles (única referencia)
            'SI',             # activo
            '',               # ultimo_acceso
            now,
            now
        ]
        
        service.append_row(sheet_name, user_data)
        nombre_completo = f"{titulo} {user['nombre']}".strip() if titulo else user['nombre']
        print(f"✅ Usuario creado: {nombre_completo} (DNI: {user['dni']}, Rol: {rol_codigo} -> {rol_id})")
        created_count += 1
        time.sleep(0.5)  # Evitar límite de cuota
    
    print(f"\n📊 Resumen: {created_count} usuarios creados, {skipped_count} omitidos")
    return created_count

def create_test_employees():
    """Crea registros de personal de prueba en RRHH."""
    service = GoogleSheetsService()
    
    # Asegurar que la hoja exista
    employee_headers = [
        'id', 'dni', 'nombres', 'apellidos', 'fecha_nacimiento', 'genero',
        'direccion', 'telefono', 'correo', 'cargo', 'area', 'fecha_ingreso',
        'tipo_contrato', 'estado', 'observaciones', 'created_at', 'updated_at'
    ]
    service.ensure_sheet_exists('rrhh_personal', employee_headers)
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    test_employees = [
        # Dirección
        {
            'dni': '12345680',
            'nombres': 'Luis Alberto',
            'apellidos': 'Morales Ramos',
            'fecha_nacimiento': '1970-05-15',
            'genero': 'M',
            'direccion': 'Av. Los Héroes 456, Lima',
            'telefono': '999111222',
            'correo': 'lmorales@drelm.gob.pe',
            'cargo': 'Director',
            'area': 'Dirección Regional',
            'fecha_ingreso': '2020-01-15',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '12345681',
            'nombres': 'Carlos Eduardo',
            'apellidos': 'Vega Salazar',
            'fecha_nacimiento': '1975-08-22',
            'genero': 'M',
            'direccion': 'Jr. Las Flores 789, Lima',
            'telefono': '999222333',
            'correo': 'cvega@drelm.gob.pe',
            'cargo': 'Subdirector',
            'area': 'Dirección Regional',
            'fecha_ingreso': '2018-03-10',
            'tipo_contrato': 'Nombrado',
        },
        # RRHH
        {
            'dni': '12345675',
            'nombres': 'María Elena',
            'apellidos': 'Vargas Rojas',
            'fecha_nacimiento': '1980-03-10',
            'genero': 'F',
            'direccion': 'Calle Las Palmas 123, Lima',
            'telefono': '999333444',
            'correo': 'mvargas@drelm.gob.pe',
            'cargo': 'Jefe de Recursos Humanos',
            'area': 'Recursos Humanos',
            'fecha_ingreso': '2015-06-01',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '45678901',
            'nombres': 'Gladys Milagros',
            'apellidos': 'Flores Quispe',
            'fecha_nacimiento': '1985-11-20',
            'genero': 'F',
            'direccion': 'Av. Colonial 567, Callao',
            'telefono': '999444555',
            'correo': 'gflores@drelm.gob.pe',
            'cargo': 'Especialista en Planillas',
            'area': 'Recursos Humanos',
            'fecha_ingreso': '2017-02-15',
            'tipo_contrato': 'CAS',
        },
        {
            'dni': '45678902',
            'nombres': 'José Luis',
            'apellidos': 'Mamani Condori',
            'fecha_nacimiento': '1988-07-05',
            'genero': 'M',
            'direccion': 'Jr. Puno 890, Lima',
            'telefono': '999555666',
            'correo': 'jmamani@drelm.gob.pe',
            'cargo': 'Analista de Personal',
            'area': 'Recursos Humanos',
            'fecha_ingreso': '2019-08-20',
            'tipo_contrato': 'CAS',
        },
        # Bienestar Social
        {
            'dni': '12345676',
            'nombres': 'Carmen Rosa',
            'apellidos': 'Díaz Mendoza',
            'fecha_nacimiento': '1978-12-25',
            'genero': 'F',
            'direccion': 'Av. Brasil 234, Lima',
            'telefono': '999666777',
            'correo': 'cdiaz@drelm.gob.pe',
            'cargo': 'Jefe de Bienestar Social',
            'area': 'Bienestar Social',
            'fecha_ingreso': '2016-04-10',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '45678903',
            'nombres': 'Sandra Elizabeth',
            'apellidos': 'Rojas Paredes',
            'fecha_nacimiento': '1990-02-14',
            'genero': 'F',
            'direccion': 'Calle Cusco 456, Lima',
            'telefono': '999777888',
            'correo': 'srojas@drelm.gob.pe',
            'cargo': 'Asistenta Social',
            'area': 'Bienestar Social',
            'fecha_ingreso': '2020-01-10',
            'tipo_contrato': 'CAS',
        },
        # Secretaría / Trámite Documentario
        {
            'dni': '12345677',
            'nombres': 'Patricia Luz',
            'apellidos': 'Fernández Quispe',
            'fecha_nacimiento': '1982-06-18',
            'genero': 'F',
            'direccion': 'Jr. Moquegua 678, Lima',
            'telefono': '999888999',
            'correo': 'pfernandez@drelm.gob.pe',
            'cargo': 'Secretaria Ejecutiva',
            'area': 'Dirección Regional',
            'fecha_ingreso': '2014-09-01',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '12345678',
            'nombres': 'Rosa María',
            'apellidos': 'Huamán Chávez',
            'fecha_nacimiento': '1986-09-30',
            'genero': 'F',
            'direccion': 'Av. Arequipa 901, Miraflores',
            'telefono': '999999111',
            'correo': 'rhuaman@drelm.gob.pe',
            'cargo': 'Técnico Administrativo',
            'area': 'Trámite Documentario',
            'fecha_ingreso': '2018-11-15',
            'tipo_contrato': 'CAS',
        },
        {
            'dni': '12345679',
            'nombres': 'Ana Lucía',
            'apellidos': 'Paredes Valverde',
            'fecha_nacimiento': '1992-04-22',
            'genero': 'F',
            'direccion': 'Calle Lima 234, San Isidro',
            'telefono': '998111222',
            'correo': 'aparedes@drelm.gob.pe',
            'cargo': 'Recepcionista',
            'area': 'Trámite Documentario',
            'fecha_ingreso': '2021-03-01',
            'tipo_contrato': 'CAS',
        },
        # Vigilancia
        {
            'dni': '12345671',
            'nombres': 'Juan Carlos',
            'apellidos': 'Pérez García',
            'fecha_nacimiento': '1975-01-10',
            'genero': 'M',
            'direccion': 'Jr. Tacna 567, Lima',
            'telefono': '998222333',
            'correo': 'jperez@drelm.gob.pe',
            'cargo': 'Vigilante',
            'area': 'Seguridad',
            'fecha_ingreso': '2012-05-01',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '12345672',
            'nombres': 'Miguel Ángel',
            'apellidos': 'López Torres',
            'fecha_nacimiento': '1980-08-15',
            'genero': 'M',
            'direccion': 'Av. Grau 890, La Victoria',
            'telefono': '998333444',
            'correo': 'mlopez@drelm.gob.pe',
            'cargo': 'Vigilante',
            'area': 'Seguridad',
            'fecha_ingreso': '2015-07-20',
            'tipo_contrato': 'CAS',
        },
        {
            'dni': '12345673',
            'nombres': 'Roberto',
            'apellidos': 'Sánchez Medina',
            'fecha_nacimiento': '1978-04-05',
            'genero': 'M',
            'direccion': 'Jr. Ayacucho 123, Breña',
            'telefono': '998444555',
            'correo': 'rsanchez@drelm.gob.pe',
            'cargo': 'Vigilante',
            'area': 'Seguridad',
            'fecha_ingreso': '2017-01-15',
            'tipo_contrato': 'CAS',
        },
        {
            'dni': '12345674',
            'nombres': 'Fernando José',
            'apellidos': 'Ramírez Castro',
            'fecha_nacimiento': '1973-11-25',
            'genero': 'M',
            'direccion': 'Av. Abancay 456, Lima',
            'telefono': '998555666',
            'correo': 'framirez@drelm.gob.pe',
            'cargo': 'Coordinador de Vigilancia',
            'area': 'Seguridad',
            'fecha_ingreso': '2010-02-01',
            'tipo_contrato': 'Nombrado',
        },
        # Patrimonio
        {
            'dni': '12345682',
            'nombres': 'Jorge Antonio',
            'apellidos': 'Silva Mendoza',
            'fecha_nacimiento': '1977-07-12',
            'genero': 'M',
            'direccion': 'Calle Piura 789, Jesús María',
            'telefono': '998666777',
            'correo': 'jsilva@drelm.gob.pe',
            'cargo': 'Jefe de Patrimonio',
            'area': 'Patrimonio',
            'fecha_ingreso': '2013-04-15',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '45678904',
            'nombres': 'Marco Antonio',
            'apellidos': 'Huanca Quispe',
            'fecha_nacimiento': '1989-03-18',
            'genero': 'M',
            'direccion': 'Jr. Huallaga 321, Lima',
            'telefono': '998777888',
            'correo': 'mhuanca@drelm.gob.pe',
            'cargo': 'Técnico en Patrimonio',
            'area': 'Patrimonio',
            'fecha_ingreso': '2019-06-01',
            'tipo_contrato': 'CAS',
        },
        # Abastecimiento
        {
            'dni': '12345683',
            'nombres': 'Pedro Pablo',
            'apellidos': 'Romero Flores',
            'fecha_nacimiento': '1976-09-08',
            'genero': 'M',
            'direccion': 'Av. Salaverry 654, San Isidro',
            'telefono': '998888999',
            'correo': 'promero@drelm.gob.pe',
            'cargo': 'Jefe de Abastecimiento',
            'area': 'Abastecimiento',
            'fecha_ingreso': '2014-01-20',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '45678905',
            'nombres': 'Diana Carolina',
            'apellidos': 'Vásquez Pinto',
            'fecha_nacimiento': '1991-12-03',
            'genero': 'F',
            'direccion': 'Jr. Carabaya 987, Lima',
            'telefono': '997111222',
            'correo': 'dvasquez@drelm.gob.pe',
            'cargo': 'Analista de Compras',
            'area': 'Abastecimiento',
            'fecha_ingreso': '2020-08-15',
            'tipo_contrato': 'CAS',
        },
        # OCI
        {
            'dni': '12345684',
            'nombres': 'Silvia Elena',
            'apellidos': 'Torres Acuña',
            'fecha_nacimiento': '1972-05-20',
            'genero': 'F',
            'direccion': 'Av. Javier Prado 1234, San Borja',
            'telefono': '997222333',
            'correo': 'storres@drelm.gob.pe',
            'cargo': 'Jefe OCI',
            'area': 'Órgano de Control Institucional',
            'fecha_ingreso': '2019-01-02',
            'tipo_contrato': 'Designado',
        },
        {
            'dni': '45678906',
            'nombres': 'Walter Eduardo',
            'apellidos': 'Ccama Apaza',
            'fecha_nacimiento': '1984-10-28',
            'genero': 'M',
            'direccion': 'Jr. Ayacucho 567, Lince',
            'telefono': '997333444',
            'correo': 'wccama@drelm.gob.pe',
            'cargo': 'Auditor',
            'area': 'Órgano de Control Institucional',
            'fecha_ingreso': '2019-07-15',
            'tipo_contrato': 'CAS',
        },
        # Personal adicional de diferentes áreas
        {
            'dni': '45678907',
            'nombres': 'Julio César',
            'apellidos': 'Mendoza Aquino',
            'fecha_nacimiento': '1983-02-28',
            'genero': 'M',
            'direccion': 'Calle Loreto 432, Pueblo Libre',
            'telefono': '997444555',
            'correo': 'jmendoza@drelm.gob.pe',
            'cargo': 'Especialista en Educación',
            'area': 'Gestión Pedagógica',
            'fecha_ingreso': '2016-03-01',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '45678908',
            'nombres': 'Luz Marina',
            'apellidos': 'Ríos Calderón',
            'fecha_nacimiento': '1987-06-14',
            'genero': 'F',
            'direccion': 'Av. Universitaria 876, San Martín de Porres',
            'telefono': '997555666',
            'correo': 'lrios@drelm.gob.pe',
            'cargo': 'Especialista en Educación',
            'area': 'Gestión Pedagógica',
            'fecha_ingreso': '2018-04-10',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '45678909',
            'nombres': 'Oscar Raúl',
            'apellidos': 'Ticona Mamani',
            'fecha_nacimiento': '1979-08-22',
            'genero': 'M',
            'direccion': 'Jr. Lampa 543, Lima',
            'telefono': '997666777',
            'correo': 'oticona@drelm.gob.pe',
            'cargo': 'Contador',
            'area': 'Contabilidad',
            'fecha_ingreso': '2011-09-15',
            'tipo_contrato': 'Nombrado',
        },
        {
            'dni': '45678910',
            'nombres': 'Karina Soledad',
            'apellidos': 'Espinoza Meza',
            'fecha_nacimiento': '1993-01-08',
            'genero': 'F',
            'direccion': 'Calle Los Olivos 234, Los Olivos',
            'telefono': '997777888',
            'correo': 'kespinoza@drelm.gob.pe',
            'cargo': 'Asistente Contable',
            'area': 'Contabilidad',
            'fecha_ingreso': '2021-06-01',
            'tipo_contrato': 'CAS',
        },
        {
            'dni': '45678911',
            'nombres': 'Héctor Manuel',
            'apellidos': 'Choque Vilca',
            'fecha_nacimiento': '1981-11-17',
            'genero': 'M',
            'direccion': 'Av. Túpac Amaru 1567, Comas',
            'telefono': '997888999',
            'correo': 'hchoque@drelm.gob.pe',
            'cargo': 'Tesorero',
            'area': 'Tesorería',
            'fecha_ingreso': '2013-08-01',
            'tipo_contrato': 'Nombrado',
        },
    ]
    
    sheet_name = 'rrhh_personal'
    existing_records = service.get_all_records(sheet_name)
    existing_dnis = {str(r.get('dni', '')) for r in existing_records}
    
    created_count = 0
    skipped_count = 0
    
    for emp in test_employees:
        if emp['dni'] in existing_dnis:
            print(f"⏭️  Empleado '{emp['nombres']} {emp['apellidos']}' (DNI: {emp['dni']}) ya existe. Omitiendo...")
            skipped_count += 1
            continue
        
        employee_id = str(uuid.uuid4())
        
        row_data = [
            employee_id,
            emp['dni'],
            emp['nombres'],
            emp['apellidos'],
            emp['fecha_nacimiento'],
            emp['genero'],
            emp['direccion'],
            emp['telefono'],
            emp['correo'],
            emp['cargo'],
            emp['area'],
            emp['fecha_ingreso'],
            emp['tipo_contrato'],
            'ACTIVO',
            '',  # observaciones
            now,
            now
        ]
        
        service.append_row(sheet_name, row_data)
        print(f"✅ Empleado creado: {emp['nombres']} {emp['apellidos']} ({emp['cargo']} - {emp['area']})")
        created_count += 1
    
    print(f"\n📊 Resumen: {created_count} empleados creados, {skipped_count} omitidos")
    return created_count

def create_test_citas():
    """Crea citas de prueba para el sistema de gestión de citas."""
    service = GoogleSheetsService()
    import json
    
    # Asegurar que la hoja exista
    headers = [
        'id', 'dni', 'oficina', 'apellidos', 'nombres', 'fecha', 
        'celular', 'hora', 'correo', 'asunto', 'estado', 'historial_json', 'created_at'
    ]
    service.ensure_sheet_exists('citas', headers)
    
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (now + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    
    test_citas = [
        {
            'dni': '78901234',
            'oficina': 'Dirección Regional',
            'apellidos': 'Gutiérrez Soto',
            'nombres': 'Alberto',
            'fecha': today,
            'celular': '987654321',
            'hora': '09:00',
            'correo': 'alberto.gutierrez@gmail.com',
            'asunto': 'Consulta sobre reconocimiento de años de servicio',
            'estado': 'PENDIENTE'
        },
        {
            'dni': '78901235',
            'oficina': 'Recursos Humanos',
            'apellidos': 'Castillo Vega',
            'nombres': 'Lucía Marina',
            'fecha': today,
            'celular': '987654322',
            'hora': '10:30',
            'correo': 'lucia.castillo@hotmail.com',
            'asunto': 'Trámite de resolución de nombramiento',
            'estado': 'ATENDIDO'
        },
        {
            'dni': '78901236',
            'oficina': 'Bienestar Social',
            'apellidos': 'Rivera Quispe',
            'nombres': 'José Antonio',
            'fecha': today,
            'celular': '987654323',
            'hora': '11:00',
            'correo': 'jose.rivera@yahoo.com',
            'asunto': 'Solicitud de atención médica',
            'estado': 'PENDIENTE'
        },
        {
            'dni': '78901237',
            'oficina': 'Trámite Documentario',
            'apellidos': 'Palacios Mendoza',
            'nombres': 'María del Carmen',
            'fecha': tomorrow,
            'celular': '987654324',
            'hora': '08:30',
            'correo': 'maria.palacios@gmail.com',
            'asunto': 'Entrega de documentos para expediente',
            'estado': 'PENDIENTE'
        },
        {
            'dni': '78901238',
            'oficina': 'Patrimonio',
            'apellidos': 'Acosta Luna',
            'nombres': 'Ricardo',
            'fecha': tomorrow,
            'celular': '987654325',
            'hora': '14:00',
            'correo': 'ricardo.acosta@outlook.com',
            'asunto': 'Consulta sobre bienes institucionales',
            'estado': 'PENDIENTE'
        },
        {
            'dni': '78901239',
            'oficina': 'Órgano de Control Institucional',
            'apellidos': 'Torres Benítez',
            'nombres': 'Elena',
            'fecha': next_week,
            'celular': '987654326',
            'hora': '09:30',
            'correo': 'elena.torres@gmail.com',
            'asunto': 'Presentación de descargos',
            'estado': 'PENDIENTE'
        },
        {
            'dni': '78901240',
            'oficina': 'Gestión Pedagógica',
            'apellidos': 'Núñez Carpio',
            'nombres': 'Fernando Luis',
            'fecha': next_week,
            'celular': '987654327',
            'hora': '10:00',
            'correo': 'fernando.nunez@hotmail.com',
            'asunto': 'Coordinación de capacitación docente',
            'estado': 'PENDIENTE'
        },
        {
            'dni': '78901241',
            'oficina': 'Abastecimiento',
            'apellidos': 'Quiroz Delgado',
            'nombres': 'Sandra Patricia',
            'fecha': today,
            'celular': '987654328',
            'hora': '15:00',
            'correo': 'sandra.quiroz@gmail.com',
            'asunto': 'Consulta sobre proceso de licitación',
            'estado': 'CANCELADO'
        },
    ]
    
    sheet_name = 'citas'
    created_count = 0
    
    for cita in test_citas:
        cita_id = str(uuid.uuid4())
        created_at = now.strftime("%Y-%m-%d %H:%M:%S")
        
        historial = [
            {'estado': cita['estado'], 'fecha': created_at, 'descripcion': f"Cita registrada - {cita['estado']}"}
        ]
        
        row_data = [
            cita_id,
            cita['dni'],
            cita['oficina'],
            cita['apellidos'],
            cita['nombres'],
            cita['fecha'],
            cita['celular'],
            cita['hora'],
            cita['correo'],
            cita['asunto'],
            cita['estado'],
            json.dumps(historial),
            created_at
        ]
        
        service.append_row(sheet_name, row_data)
        print(f"✅ Cita creada: {cita['nombres']} {cita['apellidos']} - {cita['oficina']} ({cita['fecha']} {cita['hora']})")
        created_count += 1
    
    print(f"\n📊 Resumen: {created_count} citas creadas")
    return created_count

def main():
    print("=" * 60)
    print("🚀 GENERADOR DE DATOS DE PRUEBA - DRE Sistema Control")
    print("=" * 60)
    print()
    
    print("📌 Creando tabla maestra de ROLES...")
    print("-" * 40)
    role_mapping = create_roles_table()
    print()
    
    # Esperar un poco para evitar límite de cuota
    print("⏳ Esperando 5 segundos para evitar límite de API...")
    time.sleep(5)
    
    print("📌 Creando usuarios del sistema (con FK a roles)...")
    print("-" * 40)
    create_test_users(role_mapping)
    print()
    
    # Esperar un poco para evitar límite de cuota
    print("⏳ Esperando 5 segundos para evitar límite de API...")
    time.sleep(5)
    
    print("📌 Creando registros de personal RRHH...")
    print("-" * 40)
    create_test_employees()
    print()
    
    # Esperar un poco para evitar límite de cuota
    print("⏳ Esperando 5 segundos para evitar límite de API...")
    time.sleep(5)
    
    print("📌 Creando citas de prueba...")
    print("-" * 40)
    create_test_citas()
    print()
    
    print("=" * 60)
    print("✨ ¡Proceso completado!")
    print("=" * 60)
    print()
    print("📋 ESTRUCTURA RELACIONAL CREADA:")
    print("-" * 40)
    print("• Tabla 'roles': Tabla maestra con 15 roles definidos")
    print("• Tabla 'usuarios': Con rol_id como FK a la tabla roles")
    print("• Tabla 'rrhh_personal': Registros de personal")
    print("• Tabla 'citas': Citas de prueba")
    print()
    print("📋 CREDENCIALES DE ACCESO:")
    print("-" * 60)
    print("| Rol                    | DNI      | Contraseña          | rol_id |")
    print("|------------------------|----------|---------------------|--------|")
    print("| Vigilante              | 12345671 | vigilante123        | ROL007 |")
    print("| Vigilante              | 12345672 | vigilante123        | ROL007 |")
    print("| Vigilante              | 12345673 | vigilante123        | ROL007 |")
    print("| Coord. Vigilante       | 12345674 | coordinador123      | ROL006 |")
    print("| Jefe RRHH              | 12345675 | rrhh123             | ROL004 |")
    print("| Jefe Bienestar Social  | 12345676 | bienestar123        | ROL005 |")
    print("| Secretario             | 12345677 | secretaria123       | ROL008 |")
    print("| Secretario             | 12345678 | secretaria123       | ROL008 |")
    print("| Secretario             | 12345679 | secretaria123       | ROL008 |")
    print("| Director               | 12345680 | director123         | ROL002 |")
    print("| Subdirector            | 12345681 | subdirector123      | ROL003 |")
    print("| Jefe Patrimonio        | 12345682 | patrimonio123       | ROL009 |")
    print("| Jefe Abastecimiento    | 12345683 | abastecimiento123   | ROL010 |")
    print("| Jefe OCI               | 12345684 | oci123              | ROL011 |")
    print("-" * 60)


if __name__ == "__main__":
    main()
