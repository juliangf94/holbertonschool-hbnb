#!/usr/bin/python3
from app.extensions import db
from app.models.base_model import BaseModel
from app.models.amenity import Amenity
from app.models.user import User


# Table d'association pour les places et les amenities (many-to-many)
place_amenity_association = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel, db.Model):
    __tablename__ = "places"

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Relation avec l'utilisateur (owner)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('places', lazy=True))

    # Relation many-to-many avec les amenities
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity_association,
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

    def __init__(self, title, price, latitude, longitude, owner_id, description="", **kwargs):
        super().__init__(**kwargs)

        if not title or not title.strip() or len(title.strip()) > 100:
            raise ValueError("Place title is required and cannot exceed 100 characters")
        if description and len(description) > 255:
            raise ValueError("Place description cannot exceed 255 characters")
        if price < 0:
            raise ValueError("Price must be non-negative")

        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    def update_place(self, data):
        """
        Met à jour les attributs de la place
        """
        if "title" in data:
            title = data["title"]
            if not title or not title.strip() or len(title.strip()) > 100:
                raise ValueError("Place title cannot be empty or exceed 100 characters")
            data["title"] = title.strip()

        if "description" in data:
            description = data["description"]
            if description and len(description) > 255:
                raise ValueError("Place description cannot exceed 255 characters")
            data["description"] = description.strip() if description else ""

        if "price" in data:
            price = data["price"]
            if price < 0:
                raise ValueError("Price must be non-negative")

        if "latitude" in data:
            data["latitude"] = data["latitude"]

        if "longitude" in data:
            data["longitude"] = data["longitude"]

        self.update(data)

    def __repr__(self):
        return f"<Place id={self.id} title={self.title}>"
