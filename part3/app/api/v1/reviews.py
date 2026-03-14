from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from part3.app.facade.facade import Facade

api = Namespace("reviews", description="Reviews operations")
facade = Facade()

@api.route("/")
class ReviewList(Resource):
    def get(self):
        reviews = facade.get_all_reviews()
        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
            } for review in reviews
        ], 200

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        data["user_id"] = current_user_id

        review = facade.create_review(data)
        return {
            "message": "Review created successfully",
            "review": {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
            }
        }, 201

@api.route("/<string:review_id>")
class ReviewDetail(Resource):
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id
        }, 200

    @jwt_required()
    def put(self, review_id):
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.get_json()
        updated_review = facade.update_review(review_id, data)
        return {
            "message": "Review updated successfully",
            "review": {
                "id": updated_review.id,
                "text": updated_review.text,
                "rating": updated_review.rating,
                "user_id": updated_review.user_id,
                "place_id": updated_review.place_id
            }
        }, 200

    @jwt_required()
    def delete(self, review_id):
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
