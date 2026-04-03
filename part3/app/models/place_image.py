#!/usr/bin/python3
from app.extensions import db
from app.models.base_model import BaseModel


class PlaceImage(BaseModel):
    __tablename__ = 'place_images'

    place_id  = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
