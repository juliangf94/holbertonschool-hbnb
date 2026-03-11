#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.api.v1.admin import admin_required

users_ns = Namespace("users", description="User operations")

# Modèle pour Swagger / validation
user_model = users_ns.model("User", {
    "email": fields.String(required=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "password": fields.String(required=True)
})

update_model = users_ns.model("UserUpdate", {
    "email": fields.String(),
    "first_name": fields.String(),
    "last_name": fields.String(),
    "password": fields.String()
})

# ----------------- LIST / CREATE -----------------
@users_ns.route("/")
class UserList(Resource):

    @admin_required
    @users_ns.response(200, 'List of users')
    def get(self):
        """Lister tous les utilisateurs (Admin only)"""
        users = facade.get_all_users()
        return [{
            "id": u.id,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name
        } for u in users], 200

    @admin_required
    @users_ns.expect(user_model, validate=True)
    @users_ns.response(201, 'User created successfully')
    @users_ns.response(400, 'Email already registered')
    def post(self):
        """Créer un nouvel utilisateur (Admin only)"""
        data = users_ns.payload

        if facade.get_user_by_email(data["email"]):
            return {"error": "Email already registered"}, 400

        new_user = facade.create_user(data)
        return {
            "id": new_user.id,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }, 201


# ----------------- GET / MODIFY / DELETE -----------------
@users_ns.route("/<string:user_id>")
class UserDetail(Resource):

    @jwt_required()
    @users_ns.response(200, 'User details')
    @users_ns.response(404, 'User not found')
    def get(self, user_id):
        """Récupérer un utilisateur par ID"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }, 200

    @jwt_required()
    @users_ns.response(200, 'User updated successfully')
    @users_ns.response(403, 'Unauthorized action')
    @users_ns.response(404, 'User not found')
    @users_ns.response(400, 'Email already in use')
    def put(self, user_id):
        """Modifier un utilisateur (owner ou admin)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get("is_admin", False)
        requester_id = str(current_user.get("id"))

        # ✅ Seul l'owner ou un admin peut modifier
        if not is_admin and requester_id != user_id:
            return {"error": "Unauthorized action"}, 403

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = users_ns.payload

        if "email" in data:
            existing = facade.get_user_by_email(data["email"])
            if existing and str(existing.id) != user_id:
                return {"error": "Email already in use"}, 400

        updated_user = facade.update_user(user_id, data)
        return {
            "id": updated_user.id,
            "email": updated_user.email,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name
        }, 200

    @admin_required
    @users_ns.response(200, 'User deleted successfully')
    @users_ns.response(404, 'User not found')
    def delete(self, user_id):
        """Supprimer un utilisateur (Admin only)"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        facade.delete_user(user_id)
        return {"message": "User deleted successfully"}, 200
