#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns

def create_app():
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'  # Swagger UI accessible ici
    )

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    # Placeholder: Add other namespaces later (places, reviews, amenities)
    return app

# Instantiating the app here causes circular imports. 
# In the Application Factory pattern, this must be done inside run.py.
"""
# Crée l'application pour lancer directement avec run.py
app = create_app()
"""
