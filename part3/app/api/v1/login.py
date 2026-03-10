# -*- coding: utf-8 -*-
#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import create_access_token
from app.services import get_facade
facade = get_facade()

api = Namespace('auth', description='Authentication operations')

# Modèle pour Swagger et validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid email or password')
    def post(self):
        """Authenticate a user and return a JWT token"""
        data = api.payload

        user = facade.get_user_by_email(data.get("email"))

        if not user or not user.verify_password(data.get("password")):
            return {"msg": "Invalid email or password"}, 401

        # Créer le token JWT
        access_token = create_access_token(identity={
            "id": str(user.id),
            "email": user.email,
            "is_admin": user.is_admin
        })

        return {"access_token": access_token}, 200
