from flask import Flask, render_template, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuración para servir el frontend desde Flask
frontend_folder = os.path.join(os.getcwd(), 'frontend/dist')

app = Flask(__name__, static_folder=frontend_folder, static_url_path='/')
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '6d4ffae0888e1d0f492aba5dbc8d6312455dca98b00f34a9cf1b2f9b7dccdc8e')

from routes.auth_routes import auth_bp
from routes.occurrence_routes import occurrence_bp
from routes.entry_exit_routes import entry_exit_bp
from routes.visitor_routes import visitor_bp
from routes.report_routes import report_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(occurrence_bp, url_prefix='/occurrence')
app.register_blueprint(entry_exit_bp, url_prefix='/entry_exit')
app.register_blueprint(visitor_bp, url_prefix='/visitor')
app.register_blueprint(report_bp, url_prefix='/report')
from routes.vehicle_routes import vehicle_bp
app.register_blueprint(vehicle_bp, url_prefix='/vehicle')

from routes.cita_routes import cita_bp
app.register_blueprint(cita_bp, url_prefix='/citas')

from routes.license_routes import license_bp
app.register_blueprint(license_bp, url_prefix='/license')

from routes.hr_routes import hr_bp
app.register_blueprint(hr_bp, url_prefix='/hr')

from routes.turn_routes import turn_bp
app.register_blueprint(turn_bp, url_prefix='/turn')

# Serve React/Vue Static Files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
