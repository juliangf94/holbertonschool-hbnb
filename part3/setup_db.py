#!/usr/bin/python3
"""
Script pour initialiser la base de données et créer l'utilisateur admin par défaut.
"""

from app import create_app
from app.extensions import db
from app.services import facade

def main():
    app = create_app()

    with app.app_context():
        # Crée toutes les tables
        db.create_all()
        print("Tables de la base de données créées avec succès !")

        # Vérifie si l'admin existe déjà
        admin_email = "admin@example.com"
        if not facade.get_user_by_email(admin_email):
            facade.create_user({
                "first_name": "Admin",
                "last_name": "User",
                "email": admin_email,
                "password": "adminpass",
                "is_admin": True
            })
            print("Admin créé avec succès !")
        else:
            print("Admin déjà existant — création ignorée.")

if __name__ == "__main__":
    main()