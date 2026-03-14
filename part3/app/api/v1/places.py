#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Modèle pour validation et Swagger
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='Owner user ID')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(),
    'price': fields.Float(),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
    'description': fields.String()
})

# ------------------- Liste / Création -------------------
@api.route('/')
class PlaceList(Resource):

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Lister tous les places (accessible à tous)"""
        places = facade.get_all_places()
        return [{
            'id': p.id,
            'title': p.title,
            'price': p.price,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'owner_id': p.owner_id
        } for p in places], 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Créer un nouveau place"""

        current_user_id = get_jwt_identity()
        data = api.payload
        data['owner_id'] = current_user_id

        try:
            new_place = facade.create_place(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_place.id,
            'title': new_place.title,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner_id
        }, 201


# ------------------- Détail / Mise à jour / Suppression -------------------
@api.route('/<string:place_id>')
class PlaceDetail(Resource):

    @api.response(200, 'Place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Récupérer un place par ID (accessible à tous)"""
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id
        }, 200

    @jwt_required()
    @api.expect(place_update_model, validate=False)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Mettre à jour un place (owner ou admin)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = str(current_user.get('id'))

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload
        try:
            updated_place = facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'message': 'Place updated successfully',
            'place': {
                'id': updated_place.id,
                'title': updated_place.title,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner_id
            }
        }, 200

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Supprimer un place (owner ou admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200
