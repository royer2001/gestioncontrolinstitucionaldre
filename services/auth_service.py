import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from config import Config
from services.google_sheets import GoogleSheetsService
import hashlib

class AuthService:
    def __init__(self):
        self.sheets_service = GoogleSheetsService()

    def login(self, dni, password):
        # Validate DNI format
        if not dni or not dni.isdigit() or len(dni) != 8:
            return None

        users = self.sheets_service.get_all_records('usuarios')
        # Simple hash check (in production, use bcrypt)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        for user in users:
            # La columna 'dni' contiene el DNI del usuario
            if str(user.get('dni', '')) == dni and user.get('contraseña_hash', '') == password_hash:
                token = self.generate_token(user['id'], user.get('rol_id', ''))
                return {'token': token, 'user': user}
        return None

    def generate_token(self, user_id, role):
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]
            
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            
            try:
                data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                current_user = data
            except:
                return jsonify({'message': 'Token is invalid!'}), 401
            
            return f(current_user, *args, **kwargs)
        return decorated
