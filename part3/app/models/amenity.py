#!/usr/bin/python3
from app.extensions import db
from app.models.base_model import BaseModel


class Amenity(BaseModel, db.Model):
    __tablename__ = "amenities"

    id = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), default="")

    def __init__(self, name, description="", **kwargs):
        super().__init__(**kwargs)

        # Validation du nom
        if not name or not name.strip() or len(name.strip()) > 50:
            raise ValueError("Amenity name is required and cannot exceed 50 characters")

        # Validation de la description
        if description and len(description) > 255:
            raise ValueError("Amenity description cannot exceed 255 characters")

        self.name = name.strip()
        self.description = description.strip() if description else ""

    def update_amenity(self, data):
        """
        Met à jour les attributs name et description
        """
        if "name" in data:
            name = data["name"]
            if not name or not name.strip():
                raise ValueError("Amenity name cannot be empty")
            if len(name.strip()) > 50:
                raise ValueError("Amenity name cannot exceed 50 characters")
            data["name"] = name.strip()

        if "description" in data:
            description = data["description"]
            if description and len(description) > 255:
                raise ValueError("Amenity description cannot exceed 255 characters")
            data["description"] = description.strip() if description else ""

        # Appel à la méthode générique de BaseModel
        self.update(data)

    def __repr__(self):
        return f"<Amenity id={self.id} name={self.name}>"
