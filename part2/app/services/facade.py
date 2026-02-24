#!/usr/bin/python3
from abc import ABC, abstractmethod
from xml.dom import UserDataHandler
from app.models.user import User

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            return obj
        return None

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (obj for obj in self._storage.values()
                if getattr(obj, attr_name, None) == attr_value),
            None
        )


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        return self._extracted_from_update_user_2(user_data)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)

        if not user:
            # Crée un nouvel utilisateur si l'ID n'existe pas
            user_data['id'] = user_id
            return self._extracted_from_update_user_2(user_data)
        # Vérifier unicité email si modifié
        if "email" in user_data:
            existing_user = self.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        # Mettre à jour l'utilisateur existant
        return self.user_repo.update(user_id, user_data)

    # TODO Rename this here and in `create_user` and `update_user`
    def _extracted_from_update_user_2(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
