#!/usr/bin/python3
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    def __init__(self, comment, rating, place_id, user_id):
        super().__init__()

        if not comment:
            raise ValueError("Comment is required")

        self.validate_rating(rating)

        if not isinstance(place_id, str):
            raise ValueError("Invalid place_id")

        if not isinstance(user_id, str):
            raise ValueError("Invalid user_id")

        self.comment = comment
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def validate_rating(self, rating):
        """Validates that rating is between 1 and 5"""
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            # Missing raise added here!
            raise ValueError("Rating must be an integer between 1 and 5")
