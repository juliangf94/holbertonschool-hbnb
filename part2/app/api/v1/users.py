#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# ------------------- UserList: GET /, POST / -------------------
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        users_list = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users]
        return users_list, 200

# ------------------- UserResource: PUT /<user_id> -------------------
@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data or email already registered')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update an existing user"""
        user_data = api.payload

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
