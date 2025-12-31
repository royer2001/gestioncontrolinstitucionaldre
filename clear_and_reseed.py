"""
Script para borrar hojas específicas y regenerar los datos con la estructura correcta.
"""
from services.google_sheets import GoogleSheetsService
import time

def delete_sheets(sheet_names):
    """Elimina las hojas especificadas del spreadsheet."""
    service = GoogleSheetsService()
    spreadsheet = service.client.open_by_key(service.sheet_id)
    
    for sheet_name in sheet_names:
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            spreadsheet.del_worksheet(worksheet)
            print(f"🗑️  Hoja '{sheet_name}' eliminada")
        except Exception as e:
            print(f"⚠️  No se pudo eliminar '{sheet_name}': {e}")
        time.sleep(1)  # Evitar límite de cuota

def main():
    print("=" * 60)
    print("🗑️  LIMPIEZA Y REGENERACIÓN DE DATOS")
    print("=" * 60)
    print()
    
    # Hojas a eliminar para regenerar con estructura correcta
    sheets_to_delete = ['usuarios', 'roles']
    
    print("📌 Eliminando hojas existentes...")
    print("-" * 40)
    delete_sheets(sheets_to_delete)
    print()
    
    print("⏳ Esperando 5 segundos antes de regenerar...")
    time.sleep(5)
    
    # Importar y ejecutar el seed
    print("📌 Regenerando datos...")
    print("-" * 40)
    from seed_test_data import create_roles_table, create_test_users
    
    role_mapping = create_roles_table()
    print()
    
    print("⏳ Esperando 5 segundos...")
    time.sleep(5)
    
    create_test_users(role_mapping)
    print()
    
    print("=" * 60)
    print("✅ ¡Proceso completado!")
    print("=" * 60)
    print()
    print("📋 ESTRUCTURA RELACIONAL:")
    print("-" * 40)
    print("Tabla 'roles' (PK: rol_id)")
    print("  └── rol_id, codigo, nombre, descripcion, nivel_acceso, permisos_json, activo")
    print()
    print("Tabla 'usuarios' (FK: rol_id -> roles.rol_id)")
    print("  └── id, titulo, nombre, dni, contraseña_hash, rol_id, activo, ultimo_acceso")
    print()

if __name__ == "__main__":
    main()
