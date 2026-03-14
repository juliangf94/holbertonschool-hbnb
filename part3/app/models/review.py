#!/usr/bin/python3
from app.extensions import db
from app.models.base_model import BaseModel


class Review(BaseModel, db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.String(60), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id, **kwargs):
        super().__init__(**kwargs)

        # Validation du texte
        if not text or not text.strip():
            raise ValueError("text is required")

        # Validation de la note
        self.validate_rating(rating)

        # Validation des IDs
        if not isinstance(place_id, str) or not place_id.strip():
            raise ValueError("Invalid place_id")
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("Invalid user_id")

        self.text = text.strip()
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def validate_rating(self, rating):
        """
        Vérifie que la note est un entier entre 1 et 5
        """
        if isinstance(rating, bool) or not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

    def update_review(self, data):
        """
        Met à jour les champs text et rating
        """
        if "text" in data:
            if not data["text"] or not data["text"].strip():
                raise ValueError("text is required")
            data["text"] = data["text"].strip()

        if "rating" in data:
            self.validate_rating(data["rating"])

        # Appel à la méthode générique de BaseModel
        self.update(data)

    def __repr__(self):
        return f"<Review id={self.id} rating={self.rating} user_id={self.user_id}>"
