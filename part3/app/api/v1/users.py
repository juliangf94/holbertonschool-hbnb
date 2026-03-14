#!/usr/bin/python3
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.facade import Facade

users_bp = Blueprint('users', __name__)

# ---------------------- REGISTER ---------------------- #
@users_bp.route('/', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        user = Facade.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            is_admin=data.get('is_admin', False)
        )
        return jsonify({'id': user.id, 'email': user.email}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# ---------------------- LOGIN ---------------------- #
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Facade.authenticate_user(data['email'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

# ---------------------- GET USER ---------------------- #
@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    user = Facade.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Les utilisateurs normaux ne peuvent voir que leurs infos
    if current_user_id != user.id:
        return jsonify({'error': 'Access forbidden'}), 403
    return jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_admin': user.is_admin
    })
