from services.vehicle_service import VehicleService
import datetime
import random

service = VehicleService()

def generate_systems():
    items = [
        'CILINDRO', 'CULATA', 'CARBURADOR', 'CARTER', 'DISTRIBUIDOR', 
        'BOMBA DE INYECCION', 'BOMBA DE GASOLINA', 'PURIFICADOR DE AIRE',
        'BOMBA DE FRENOS', 'ZAPATA Y TAMBORES', 'DISCOS Y PASTILLAS',
        'RADIADOR', 'VENTILADOR', 'BOMBA DE AGUA',
        'MOTOR DE ARRANQUE', 'BATERIA', 'ALTERNADOR', 'BOBINA', 'RELAY DE ALTERNADOR', 
        'CIRCUITO DE LUCES', 'FAROS', 'CABLEADOS',
        'CAJA DE CAMBIO', 'BOMBA DE EMBRAGUE', 'CAJA DE TRANSFERENCIA', 
        'DIFERENCIAL TRASERO', 'DIFERENCIAL DELANTERO',
        'VOLANTE', 'CANAL DE DIRECCION', 'CREMALLERA', 'ROTULAS',
        'AMORTIGUADORES', 'MUELLES', 'BARRA DE TORSION', 'BARRA ESTABILIZADORA', 'LLANTAS',
        'CAPOT DE MOTOR', 'CAPOT DE MALETERA', 'PARACHOQUE DELANTERO', 'PARACHOQUE POSTERIOR', 
        'PARABRISAS', 'LUNAS', 'TANQUE DE COMBUSTIBLE', 'PUERTAS', 'ASIENTOS',
        'AIRE ACONDICIONADO', 'ESPEJOS', 'RADIO', 'CLAXON', 'ALARMA', 'EXTINTOR', 
        'DESARMADOR', 'GATA', 'PARLANTES', 'RELOJ'
    ]
    systems = {}
    for item in items:
        systems[item] = {
            'estado': random.choice(['Bueno', 'Bueno', 'Bueno', 'Regular', 'Malo']), 
            'cantidad': '1'
        }
    return systems

samples = [
    {
        'fecha': '2024-01-15',
        'entidad': 'DRE MADRE DE DIOS',
        'denominacion': 'Camioneta Pick Up',
        'placa': 'EGF-123',
        'color': 'Blanco',
        'kilometraje': '45000',
        'carroceria': 'Metalica',
        'n_motor': 'TOY-2024-X45',
        'sistemas': generate_systems(),
        'abastecimiento': 'Juan Perez',
        'recepciona': 'Carlos Sanchez'
    },
    {
        'fecha': '2024-02-20',
        'entidad': 'DRE MADRE DE DIOS',
        'denominacion': 'Automovil Sedan',
        'placa': 'ABC-987',
        'color': 'Gris',
        'kilometraje': '120500',
        'carroceria': 'Metalica',
        'n_motor': 'NIS-98-ZZ',
        'sistemas': generate_systems(),
        'abastecimiento': 'Juan Perez',
        'recepciona': 'Maria Lopez'
    },
     {
        'fecha': '2024-03-10',
        'entidad': 'UGEL TAMBOPATA',
        'denominacion': 'Motocicleta Lineal',
        'placa': 'KT-4500',
        'color': 'Rojo',
        'kilometraje': '15000',
        'carroceria': '-',
        'n_motor': 'HON-555-M',
        'sistemas': generate_systems(),
        'abastecimiento': 'Pedro Gomez',
        'recepciona': 'Luis Fernandez'
    }
]

print("Generando datos de ejemplo para Actas de Entrega...")
try:
    for data in samples:
        service.create_handover(data)
        print(f"Acta creada para vehículo {data['placa']}")
    print("Datos generados correctamente.")
except Exception as e:
    print(f"Error al generar datos: {e}")
