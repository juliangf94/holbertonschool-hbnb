#!/usr/bin/python3

from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """
    Facade layer that connects the API (Presentation layer)
    to the Business Logic and Persistence layers.
    """

    def __init__(self):
        self.user_repo = InMemoryRepository()

    # -------------------------
    # CREATE
    # -------------------------
    def create_user(self, user_data):
        """
        Create a new user and store it in the repository.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    # -------------------------
    # READ (single user)
    # -------------------------
    def get_user(self, user_id):
        """
        Retrieve a user by ID.
        """
        return self.user_repo.get(user_id)

    # -------------------------
    # READ (by email)
    # -------------------------
    def get_user_by_email(self, email):
        """
        Retrieve a user by email.
        """
        return self.user_repo.get_by_attribute('email', email)

    # -------------------------
    # READ (all users)
    # -------------------------
    def get_all_users(self):
        """
        Retrieve all users.
        """
        return self.user_repo.get_all()

    # -------------------------
    # UPDATE
    # -------------------------
    def update_user(self, user_id, user_data):
        """
        Update an existing user.
        Returns None if user does not exist.
        Raises ValueError if email already exists.
        """
        user = self.user_repo.get(user_id)

        if not user:
            return None

        # Check email uniqueness if modified
        if "email" in user_data:
            existing_user = self.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")
        # The update operation must be outside the email condition block 
        # to ensure other attributes (like first_name) are still updated even if no email is provided.
        updated_user = self.user_repo.update(user_id, user_data)
        return updated_user
