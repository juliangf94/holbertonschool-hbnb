#!/usr/bin/python3
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # -------------------------
    # USERS CRUD
    # -------------------------
    def create_user(self, data):
        if "password" not in data or not data["password"]:
            raise ValueError("Password is required")
        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            is_admin=data.get("is_admin", False)
        )
        user.set_password(data["password"])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "email" in user_data:
            existing = self.get_user_by_email(user_data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        if "password" in user_data and user_data["password"]:
            user.set_password(user_data["password"])
            user_data.pop("password")
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # -------------------------
    # AMENITIES CRUD
    # -------------------------
    def create_amenity(self, data):
        if not data.get("name") or not data["name"].strip():
            raise ValueError("Amenity must have a non-empty name")
        existing = self.amenity_repo.get_by_attribute("name", data["name"])
        if existing:
            raise ValueError("Amenity with this name already exists")
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, data)
        return self.amenity_repo.get(amenity_id)

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # -------------------------
    # PLACES CRUD
    # -------------------------
    def create_place(self, data):
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for f in required_fields:
            if f not in data:
                raise ValueError(f"Missing required field: {f}")
        if not self.user_repo.get(data["owner_id"]):
            raise ValueError("Owner not found")
        place = Place(**data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        self.place_repo.update(place_id, data)
        return self.place_repo.get(place_id)

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # -------------------------
    # REVIEWS CRUD
    # -------------------------
    def create_review(self, data):
        required = ['text', 'rating', 'user_id', 'place_id']
        for f in required:
            if f not in data:
                raise ValueError(f"Missing required field: {f}")
        if not self.user_repo.get(data["user_id"]):
            raise ValueError("User not found")
        if not self.place_repo.get(data["place_id"]):
            raise ValueError("Place not found")
        review = Review(**data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True


# -------------------------
# Exporter l'instance du Facade
# -------------------------
facade = HBnBFacade()
