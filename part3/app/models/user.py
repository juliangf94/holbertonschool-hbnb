#!/usr/bin/python3
import re
from app.extensions import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel, db.Model):
    """
    User model for storing user information.
    """
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize a new user with validation and password hashing.
        """
        super().__init__()

        if not first_name or not first_name.strip() or len(first_name.strip()) > 50:
            raise ValueError("first_name is required and cannot exceed 50 characters")
        self.first_name = first_name.strip()

        # Validate last_name
        if not last_name or not last_name.strip() or len(last_name.strip()) > 50:
            raise ValueError("last_name is required and cannot exceed 50 characters")
        self.last_name = last_name.strip()

        # Validate email
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
            raise ValueError("Invalid email format")
        self.email = email.strip().lower()

        # Validate password
        if not password:
            raise ValueError("Password is required")
        self.set_password(password)

        # Admin flag
        self.is_admin = is_admin

    def set_password(self, password):
        """
        Hash and store the password.
        """
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """
        Verify password — utilisé dans login.py
        """
        return bcrypt.check_password_hash(self.password, password)

    def update_profile(self, data):
        """
        Update user profile with validation and optional password hashing.
        """
        if "first_name" in data:
            if not data["first_name"] or not data["first_name"].strip() or len(data["first_name"].strip()) > 50:
                raise ValueError("first_name is required and cannot exceed 50 characters")
            self.first_name = data["first_name"].strip()

        if "last_name" in data:
            if not data["last_name"] or not data["last_name"].strip() or len(data["last_name"].strip()) > 50:
                raise ValueError("last_name is required and cannot exceed 50 characters")
            self.last_name = data["last_name"].strip()

        if "email" in data:
            if not data["email"] or not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"].strip()):
                raise ValueError("Invalid email format")
            self.email = data["email"].strip().lower()

        if "password" in data and data["password"]:
            self.set_password(data["password"])
