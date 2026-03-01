#!/usr/bin/python3
import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password="", is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("Invalid first_name")

        if not last_name or len(last_name) > 50:
            raise ValueError("Invalid last_name")

        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []

    def update_profile(self, data):
        """Specific method to update user profile"""
        self.update(data)
