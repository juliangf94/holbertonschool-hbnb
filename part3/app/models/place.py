# -*- coding: utf-8 -*-
#!/usr/bin/python3
from app.extensions import db
from app.models.base_model import BaseModel


class Place(BaseModel, db.Model):
    __tablename__ = "places"

    id = db.Column(db.String(60), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, description="", price=0, latitude=0, longitude=0, owner_id=None, **kwargs):
        super().__init__()

        try:
            price = float(price)
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            raise ValueError("Price, latitude, and longitude must be valid numbers")

        if not title or not title.strip() or len(title.strip()) > 100:
            raise ValueError("Title is required and cannot exceed 100 characters")

        if description and len(description) > 1024:
            raise ValueError("Description cannot exceed 1024 characters")

        if price <= 0:
            raise ValueError("Price must be positive")

        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        if not owner_id or not str(owner_id).strip():
            raise ValueError("Invalid owner_id")

        self.title = title.strip()
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = str(owner_id)

    def update_details(self, data):
        """Update place details with validation"""
        if "title" in data:
            if not data["title"] or not data["title"].strip() or len(data["title"].strip()) > 100:
                raise ValueError("Title is required and cannot exceed 100 characters")
            data["title"] = data["title"].strip()

        if "description" in data and data["description"]:
            if len(data["description"]) > 1024:
                raise ValueError("Description cannot exceed 1024 characters")

        if "price" in data:
            try:
                data["price"] = float(data["price"])
            except (ValueError, TypeError):
                raise ValueError("Price must be a valid number")
            if data["price"] <= 0:
                raise ValueError("Price must be positive")

        if "latitude" in data:
            try:
                data["latitude"] = float(data["latitude"])
            except (ValueError, TypeError):
                raise ValueError("Latitude must be a valid number")
            if not (-90 <= data["latitude"] <= 90):
                raise ValueError("Latitude must be between -90 and 90")

        if "longitude" in data:
            try:
                data["longitude"] = float(data["longitude"])
            except (ValueError, TypeError):
                raise ValueError("Longitude must be a valid number")
            if not (-180 <= data["longitude"] <= 180):
                raise ValueError("Longitude must be between -180 and 180")

        self.update(data)
