#!/usr/bin/python3
from app.extensions import db
from app.models.base_model import BaseModel


class Amenity(BaseModel, db.Model):
    __tablename__ = "amenities"

    id = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), default="")

    def __init__(self, name, description="", **kwargs):
        super().__init__()

        if not name or not name.strip() or len(name.strip()) > 50:
            raise ValueError("Amenity name is required and cannot exceed 50 characters")

        if description and len(description) > 255:
            raise ValueError("Amenity description cannot exceed 255 characters")

        self.name = name.strip()
        self.description = description

    def update_amenity(self, data):
        if "name" in data:
            if not data["name"] or not data["name"].strip():
                raise ValueError("Amenity name cannot be empty")
            if len(data["name"].strip()) > 50:
                raise ValueError("Amenity name cannot exceed 50 characters")
            data["name"] = data["name"].strip()

        if "description" in data and data["description"]:
            if len(data["description"]) > 255:
                raise ValueError("Amenity description cannot exceed 255 characters")

        self.update(data)
