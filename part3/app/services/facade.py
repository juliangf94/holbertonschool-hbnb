# part3/app/facade.py
from app.models import db, User, Place, Review
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


class Facade:
    """Facade pour gérer les opérations CRUD de l'application."""

    # ---------------------- USERS ---------------------- #
    @staticmethod
    def create_user(first_name, last_name, email, password, is_admin=False):
        """Créer un utilisateur avec mot de passe haché."""
        hashed_password = generate_password_hash(password)
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            is_admin=is_admin
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Un utilisateur avec cet email existe déjà.")
        return user

    @staticmethod
    def get_user_by_id(user_id):
        """Récupérer un utilisateur par son ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        """Récupérer un utilisateur par son email."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update_user(user_id, **kwargs):
        """Mettre à jour les informations d'un utilisateur."""
        user = Facade.get_user_by_id(user_id)
        if not user:
            return None

        for key, value in kwargs.items():
            if key == "password":
                setattr(user, key, generate_password_hash(value))
            elif hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        """Supprimer un utilisateur."""
        user = Facade.get_user_by_id(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def authenticate_user(email, password):
        """Vérifie l'email et le mot de passe pour l'authentification."""
        user = Facade.get_user_by_email(email)
        if user and check_password_hash(user.password, password):
            return user
        return None

    # ---------------------- PLACES ---------------------- #
    @staticmethod
    def create_place(name, description, owner_id):
        """Créer un lieu."""
        place = Place(name=name, description=description, owner_id=owner_id)
        db.session.add(place)
        db.session.commit()
        return place

    @staticmethod
    def get_place_by_id(place_id):
        return Place.query.get(place_id)

    @staticmethod
    def update_place(place_id, **kwargs):
        place = Facade.get_place_by_id(place_id)
        if not place:
            return None
        for key, value in kwargs.items():
            if hasattr(place, key):
                setattr(place, key, value)
        db.session.commit()
        return place

    @staticmethod
    def delete_place(place_id):
        place = Facade.get_place_by_id(place_id)
        if not place:
            return False
        db.session.delete(place)
        db.session.commit()
        return True

    @staticmethod
    def get_places_by_owner(owner_id):
        return Place.query.filter_by(owner_id=owner_id).all()

    # ---------------------- REVIEWS ---------------------- #
    @staticmethod
    def create_review(user_id, place_id, text, rating):
        """Créer un avis pour un lieu."""
        # Optionnel : vérifier qu'un utilisateur ne peut pas reviewer plusieurs fois le même lieu
        existing_review = Review.query.filter_by(user_id=user_id, place_id=place_id).first()
        if existing_review:
            raise ValueError("Vous avez déjà publié un avis pour ce lieu.")

        review = Review(user_id=user_id, place_id=place_id, text=text, rating=rating)
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def get_review_by_id(review_id):
        return Review.query.get(review_id)

    @staticmethod
    def update_review(review_id, **kwargs):
        review = Facade.get_review_by_id(review_id)
        if not review:
            return None
        for key, value in kwargs.items():
            if hasattr(review, key):
                setattr(review, key, value)
        db.session.commit()
        return review

    @staticmethod
    def delete_review(review_id):
        review = Facade.get_review_by_id(review_id)
        if not review:
            return False
        db.session.delete(review)
        db.session.commit()
        return True

    @staticmethod
    def get_reviews_by_place(place_id):
        return Review.query.filter_by(place_id=place_id).all()

    @staticmethod
    def get_reviews_by_user(user_id):
        return Review.query.filter_by(user_id=user_id).all()
