# -*- coding: utf-8 -*-
#!/usr/bin/python3
import re
from app.extensions import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel, db.Model):
    """User model"""
    __tablename__ = "users"

    id = db.Column(db.String(60), primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        """Initialize a new user"""
        super().__init__()

        # ✅ .strip() pour rejeter les valeurs avec seulement des espaces
        if not first_name or not first_name.strip() or len(first_name.strip()) > 50:
            raise ValueError("first_name is required and cannot exceed 50 characters")

        if not last_name or not last_name.strip() or len(last_name.strip()) > 50:
            raise ValueError("last_name is required and cannot exceed 50 characters")

        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
            raise ValueError("Invalid email format")

        if not password:
            raise ValueError("Password is required")

        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.is_admin = is_admin
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify password — utilisé dans login.py"""  # ✅ Dans la classe, nom cohérent avec login.py
        return bcrypt.check_password_hash(self.password, password)

    def update_profile(self, data):
        """Update user profile with validation"""

        if "first_name" in data:
            if not data["first_name"] or not data["first_name"].strip() or len(data["first_name"].strip()) > 50:
                raise ValueError("first_name is required and cannot exceed 50 characters")
            data["first_name"] = data["first_name"].strip()

        if "last_name" in data:
            if not data["last_name"] or not data["last_name"].strip() or len(data["last_name"].strip()) > 50:
                raise ValueError("last_name is required and cannot exceed 50 characters")
            data["last_name"] = data["last_name"].strip()

        if "email" in data:
            if not data["email"] or not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"].strip()):
                raise ValueError("Invalid email format")
            data["email"] = data["email"].strip().lower()

        if "password" in data and data["password"]:
            # Hasher le nouveau mot de passe avant mise à jour
            data["password"] = bcrypt.generate_password_hash(
                data["password"]
            ).decode("utf-8")

        self.update(data)
