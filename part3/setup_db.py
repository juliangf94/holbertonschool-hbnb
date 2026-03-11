# -*- coding: utf-8 -*-
#!/usr/bin/python3
from app import create_app
from app.extensions import db
from app.services import facade

app = create_app()

with app.app_context():
    admin_email = "admin@example.com"
    if not facade.get_user_by_email(admin_email):
        facade.create_user({
            "first_name": "Admin",
            "last_name": "User",
            "email": admin_email,
            "password": "adminpass",
            "is_admin": True
        })
        print("Admin créé :", admin_email)
    else:
        print("Admin déjà présent :", admin_email)
