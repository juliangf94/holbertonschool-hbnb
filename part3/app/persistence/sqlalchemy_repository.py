# -*- coding: utf-8 -*-
#!/usr/bin/python3
from app.extensions import db
from app.persistence.repository import Repository


class SQLAlchemyRepository(Repository):
    """Repository implementation using SQLAlchemy"""

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception:
            db.session.rollback()
            raise

    def get(self, obj_id):
        return db.session.get(self.model, obj_id)
    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        try:
            obj.update(data)
            db.session.commit()
            return obj
        except Exception:
            db.session.rollback()
            raise

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return None

        try:
            db.session.delete(obj)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(
            getattr(self.model, attr_name) == attr_value
        ).first()
