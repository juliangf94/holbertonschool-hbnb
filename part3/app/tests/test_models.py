#!/usr/bin/python3
"""
HBNB Part 2 - Test suite (hold off on DB testing)
Tests the API structure and facade without persisting to DB.
"""

import sys
import os
import unittest

# Ensure Python can find the app package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class TestFacadeStructure(unittest.TestCase):
    """
    Tests the existence of methods and basic object creation.
    """

    def setUp(self):
        self.facade = HBnBFacade()

    # -------------------------
    # USERS
    # -------------------------
    def test_user_methods_exist(self):
        self.assertTrue(hasattr(self.facade, 'create_user'))
        self.assertTrue(hasattr(self.facade, 'get_user'))
        self.assertTrue(hasattr(self.facade, 'get_all_users'))

    def test_user_object_creation(self):
        data = {"first_name": "John", "last_name": "Doe", "email": "john@example.com", "password": "pass123"}
        user = User(**data)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.email, "john@example.com")

    # -------------------------
    # AMENITIES
    # -------------------------
    def test_amenity_methods_exist(self):
        self.assertTrue(hasattr(self.facade, 'create_amenity'))
        self.assertTrue(hasattr(self.facade, 'get_amenity'))
        self.assertTrue(hasattr(self.facade, 'get_all_amenities'))

    def test_amenity_object_creation(self):
        data = {"name": "WiFi"}
        amenity = Amenity(**data)
        self.assertEqual(amenity.name, "WiFi")

    # -------------------------
    # PLACES
    # -------------------------
    def test_place_methods_exist(self):
        self.assertTrue(hasattr(self.facade, 'create_place'))
        self.assertTrue(hasattr(self.facade, 'get_place'))
        self.assertTrue(hasattr(self.facade, 'get_all_places'))

    def test_place_object_creation(self):
        data = {"title": "Nice Apartment", "price": 120.0, "latitude": 48.85, "longitude": 2.35, "owner_id": "dummy"}
        place = Place(**data)
        self.assertEqual(place.title, "Nice Apartment")
        self.assertEqual(place.price, 120.0)

    # -------------------------
    # REVIEWS
    # -------------------------
    def test_review_methods_exist(self):
        self.assertTrue(hasattr(self.facade, 'create_review'))
        self.assertTrue(hasattr(self.facade, 'get_review'))
        self.assertTrue(hasattr(self.facade, 'get_all_reviews'))

    def test_review_object_creation(self):
        data = {"text": "Great!", "rating": 5, "user_id": "dummy", "place_id": "dummy"}
        review = Review(**data)
        self.assertEqual(review.text, "Great!")
        self.assertEqual(review.rating, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
