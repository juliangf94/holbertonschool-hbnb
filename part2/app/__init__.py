#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns

def create_app():
    """
    Application Factory for Flask.
    Returns a Flask app with all API namespaces registered.
    """
    app = Flask(__name__)
    
    # Create the Flask-RestX API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')
    
    # Placeholder: other namespaces like places or reviews can be added here later
    return app
    
