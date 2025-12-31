from flask import Flask, render_template, session, redirect, url_for, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuración para servir el frontend desde Flask
basedir = os.path.abspath(os.path.dirname(__file__))
frontend_folder = os.path.join(basedir, 'frontend', 'dist')

# Logging al iniciar
print(f"🚀 Base directory: {basedir}")
print(f"📁 Frontend folder: {frontend_folder}")
print(f"📁 Frontend folder exists: {os.path.exists(frontend_folder)}")

if os.path.exists(frontend_folder):
    print(f"📄 Contents of dist: {os.listdir(frontend_folder)}")
else:
    print("⚠️ WARNING: frontend/dist folder does NOT exist!")
    # Listar lo que hay en basedir para depurar
    print(f"📂 Contents of basedir: {os.listdir(basedir)}")
    frontend_check = os.path.join(basedir, 'frontend')
    if os.path.exists(frontend_check):
        print(f"📂 Contents of frontend: {os.listdir(frontend_check)}")

app = Flask(__name__, static_folder=frontend_folder, static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '6d4ffae0888e1d0f492aba5dbc8d6312455dca98b00f34a9cf1b2f9b7dccdc8e')

from routes.auth_routes import auth_bp
from routes.occurrence_routes import occurrence_bp
from routes.entry_exit_routes import entry_exit_bp
from routes.visitor_routes import visitor_bp
from routes.report_routes import report_bp

# Todas las rutas de API ahora tienen prefijo /api/
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(occurrence_bp, url_prefix='/api/occurrence')
app.register_blueprint(entry_exit_bp, url_prefix='/api/entry_exit')
app.register_blueprint(visitor_bp, url_prefix='/api/visitor')
app.register_blueprint(report_bp, url_prefix='/api/report')

from routes.vehicle_routes import vehicle_bp
app.register_blueprint(vehicle_bp, url_prefix='/api/vehicle')

from routes.cita_routes import cita_bp
app.register_blueprint(cita_bp, url_prefix='/api/citas')

from routes.license_routes import license_bp
app.register_blueprint(license_bp, url_prefix='/api/license')

from routes.hr_routes import hr_bp
app.register_blueprint(hr_bp, url_prefix='/api/hr')

from routes.turn_routes import turn_bp
app.register_blueprint(turn_bp, url_prefix='/api/turn')

# Serve Vue Static Files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Si la carpeta dist no existe, mostrar error informativo
    if not os.path.exists(app.static_folder):
        return jsonify({
            'error': 'Frontend not built',
            'message': 'La carpeta frontend/dist no existe. Verifica que el build se haya ejecutado correctamente.',
            'static_folder': app.static_folder,
            'basedir': basedir
        }), 500
    
    # Servir archivos estáticos
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return jsonify({
                'error': 'index.html not found',
                'message': 'No se encontró index.html en la carpeta dist.',
                'contents': os.listdir(app.static_folder) if os.path.exists(app.static_folder) else []
            }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
