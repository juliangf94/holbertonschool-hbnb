#!/usr/bin/python3
import os
from flask import Flask
from flask_restx import Api
from app.extensions import db, bcrypt, jwt

# Import des namespaces API
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns
from app.api.v1.admin import api as admin_ns

from config import config  # Assure-toi que config.py est dans le même dossier racine


def create_app(config_name='development'):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Charger la configuration
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)

    # Initialiser les extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Créer la base de données si elle n’existe pas
    with app.app_context():
        if not os.path.exists(os.path.join(app.root_path, 'instance')):
            os.makedirs(os.path.join(app.root_path, 'instance'))
        db.create_all()

    # Configuration Swagger / JWT
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT token. Format: Bearer <token>'
        }
    }

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        authorizations=authorizations,
        security='Bearer'
    )

    # Enregistrement des namespaces
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app
