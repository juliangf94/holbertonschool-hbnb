# -*- coding: utf-8 -*-
#!/usr/bin/python3
import uuid
from datetime import datetime


class BaseModel:
    id = None
    created_at = None
    updated_at = None

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        PROTECTED = {"id", "created_at"}
        for key, value in data.items():
            if hasattr(self, key) and key not in PROTECTED:
                setattr(self, key, value)
        self.save()

    def delete(self):
        """Placeholder for delete operation"""
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
