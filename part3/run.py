#!/usr/bin/python3

from app import create_app
from config import config

# Création de l'application Flask avec la configuration par défaut
app = create_app(config_name="default")  # ou config_name="development" selon ton config.py

# Création de l'admin user dans le contexte Flask
with app.app_context():
    from app.services import facade
    try:
        facade.create_user({
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "adminpass",
            "is_admin": True
        })
        print("Admin user created successfully")
    except ValueError:
        print("Admin user already exists — skipping")

# Lancement du serveur Flask
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
