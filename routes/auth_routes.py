from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    dni = data.get('dni')
    password = data.get('password')
    
    if not dni or not password:
         return jsonify({'message': 'DNI y contraseña son requeridos'}), 400

    result = auth_service.login(dni, password)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Credenciales inválidas o DNI incorrecto'}), 401

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
