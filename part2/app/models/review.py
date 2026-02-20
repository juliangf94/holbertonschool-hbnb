#!/usr/bin/python3
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Text is required")

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        if not isinstance(place, Place):
            raise ValueError("Invalid place")

        if not isinstance(user, User):
            raise ValueError("Invalid user")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        place.reviews.append(self)