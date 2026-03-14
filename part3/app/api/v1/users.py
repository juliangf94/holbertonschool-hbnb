#!/usr/bin/python3
from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from app.services.facade import HBnBFacade

facade = HBnBFacade()
api = Namespace("users", description="Users operations")

# Modèle pour Swagger / validation
user_model = api.model(
    "User", {
        "first_name": fields.String(required=True, description="First name"),
        "last_name": fields.String(required=True, description="Last name"),
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="Password"),
        "is_admin": fields.Boolean(description="Is admin")
    }
)

# -------------------------
# USERS COLLECTION
# -------------------------
@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [{"first_name": u.first_name,
                 "last_name": u.last_name,
                 "email": u.email,
                 "is_admin": u.is_admin} for u in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, "User created successfully")
    @api.response(400, "Invalid input or email already registered")
    def post(self):
        """Create a new user"""
        data = request.get_json()
        try:
            user = facade.create_user(data)
            return {"first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "is_admin": user.is_admin}, 201
        except ValueError as e:
            return {"message": str(e)}, 400


# -------------------------
# USER ITEM
# -------------------------
@api.route("/<string:user_id>")
class UserResource(Resource):
    @jwt_required()
    @api.response(200, "User retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get a single user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return {"first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_admin": user.is_admin}, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, "User updated successfully")
    @api.response(400, "Invalid input or email already registered")
    @api.response(404, "User not found")
    def put(self, user_id):

        """Update a user by ID"""
        user_data = request.get_json()
        try:
            user = facade.update_user(user_id, user_data)
            if not user:
                return {"message": "User not found"}, 404
            return {"first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "is_admin": user.is_admin}, 200
        except ValueError as e:
            return {"message": str(e)}, 400

        """Modifier un utilisateur (owner ou admin)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get("is_admin", False)
        requester_id = str(current_user.get("id"))

        # Seul l'owner ou un admin peut modifier
        if not is_admin and requester_id != user_id:
            return {"error": "Unauthorized action"}, 403


    @jwt_required()
    @api.response(204, "User deleted successfully")
    @api.response(404, "User not found")
    def delete(self, user_id):
        """Delete a user by ID"""
        success = facade.delete_user(user_id)
        if not success:
            return {"message": "User not found"}, 404
        return "", 204
    
