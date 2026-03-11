#!/usr/bin/python3
from app import create_app
from app.services import facade 

app = create_app()

with app.app_context():
    admin_email = "admin@example.com"

    # Vérifier si l'admin existe déjà sans le supprimer
    existing = facade.get_user_by_email(admin_email)
    if existing:
        print(f"Admin déjà existant : {admin_email}")
    else:
        admin = facade.create_user({ 
            "first_name": "Admin",
            "last_name": "User",
            "email": admin_email,
            "password": "adminpass",
            "is_admin": True
        })
        print(f"Nouvel admin créé avec succès : {admin.email}")
