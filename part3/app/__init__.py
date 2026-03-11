#!/usr/bin/python3
import os
from flask import Flask
from flask_restx import Api
from .extensions import db, bcrypt, jwt
from .models.user import User
from .models.place import Place
from .models.review import Review
from .models.amenity import Amenity
from .api.v1.users import users_ns
from .api.v1.places import api as places_ns
from .api.v1.reviews import api as reviews_ns
from .api.v1.amenities import api as amenities_ns
from .api.v1.login import api as auth_ns
from .api.v1.admin import api as admin_ns
from config import config


def create_app(config_name='default'):
    app = Flask(__name__)

    # Charger la configuration
    app.config.from_object(config[config_name])

    # Base de données SQLite par défaut (dans instance/)
    db_path = os.path.join(app.instance_path, 'development.db')
    os.makedirs(app.instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # RESTX config
    app.config['RESTX_MASK_SWAGGER'] = False

    # Clé JWT depuis l'environnement ou fallback dev
    jwt_secret = os.environ.get('JWT_SECRET_KEY', 'dev_secret_key_not_for_production')
    app.config['JWT_SECRET_KEY'] = jwt_secret

    # Initialiser les extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialisation API RESTX
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API pour HolbertonBnB'
    )

    # Ajouter les namespaces
    api.add_namespace(users_ns,     path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns,    path='/api/v1/places')
    api.add_namespace(reviews_ns,   path='/api/v1/reviews')
    api.add_namespace(auth_ns,      path='/api/v1/auth')
    api.add_namespace(admin_ns,     path='/api/v1/admin')

    # Créer les tables si elles n'existent pas
    with app.app_context():
        db.create_all()
        # Permissions du fichier DB (lecture/écriture pour tous)
        try:
            os.chmod(db_path, 0o666)
        except Exception:
            pass

    return app
