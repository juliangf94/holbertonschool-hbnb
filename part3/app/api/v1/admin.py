#!/usr/bin/python3
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from functools import wraps

api = Namespace('admin', description='Admin operations')

# -------------------------
# Décorateur RBAC pour admins
# -------------------------
def admin_required(fn):
    """Décorateur pour restreindre l'accès aux admins uniquement"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403
        return fn(*args, **kwargs)
    return jwt_required()(wrapper)  # ✅ jwt_required appliqué en dernier

# -------------------------
# Modèles pour Swagger / validation
# -------------------------
user_model = api.model('AdminUser', {  # ✅ Renommé pour éviter les conflits
    'email': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'password': fields.String(required=True)
})

amenity_model = api.model('AdminAmenity', {  # ✅ Renommé pour éviter les conflits
    'name': fields.String(required=True, description='Name of the amenity')
})

# -------------------------
# USERS
# -------------------------
@api.route('/users/')
class AdminUserCreate(Resource):
    @admin_required          # ✅ admin_required en premier
    @api.expect(user_model)
    def post(self):
        """Créer un nouvel utilisateur (admins uniquement)"""
        data = request.get_json()
        if facade.get_user_by_email(data.get("email")):
            return {"error": "Email already registered"}, 400
        new_user = facade.create_user(data)
        return new_user, 201

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @admin_required          # ✅ admin_required en premier
    @api.expect(user_model)
    def put(self, user_id):
        """Modifier un utilisateur existant (admins uniquement)"""
        data = request.get_json()
        email = data.get("email")
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {"error": "Email already in use"}, 400
        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {"error": "User not found"}, 404
        return updated_user, 200

# -------------------------
# AMENITIES
# -------------------------
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @admin_required          # ✅ admin_required en premier
    @api.expect(amenity_model)
    def post(self):
        """Créer un nouvel amenity (admins uniquement)"""
        data = request.get_json()
        new_amenity = facade.create_amenity(data)
        return new_amenity, 201

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @admin_required          # ✅ admin_required en premier
    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Modifier un amenity existant (admins uniquement)"""
        data = request.get_json()
        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            return {"error": "Amenity not found"}, 404
        return updated_amenity, 200

# -------------------------
# PLACES
# -------------------------
@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        """Modifier un place (admins peuvent bypass ownership)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        if not is_admin and place.owner_id != user_id:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json()
        updated_place = facade.update_place(place_id, data)
        return updated_place, 200

    @jwt_required()
    def delete(self, place_id):
        """Supprimer un place (admins peuvent bypass ownership)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        if not is_admin and place.owner_id != user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_place(place_id)
        return {"msg": "Place deleted"}, 200

# -------------------------
# REVIEWS
# -------------------------
@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @jwt_required()
    def put(self, review_id):
        """Modifier un review (admins peuvent bypass ownership)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if not is_admin and review.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json()
        updated_review = facade.update_review(review_id, data)
        return updated_review, 200

    @jwt_required()
    def delete(self, review_id):
        """Supprimer un review (admins peuvent bypass ownership)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if not is_admin and review.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"msg": "Review deleted"}, 200
