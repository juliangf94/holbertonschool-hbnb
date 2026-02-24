import sys
import os
# Aseguramos que Python encuentre la carpeta 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user_creation():
    user = User(first_name="Julian", last_name="Gonzalez", email="julian@example.com", password="secure_password")
    assert user.first_name == "Julian"
    assert user.email == "julian@example.com"
    assert user.password == "secure_password"
    assert user.is_admin is False
    print("✅ User creation test passed!")

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    # Pasamos owner.id en lugar del objeto owner
    place = Place(title="Apartamento en Rennes", description="Cerca del campus", price=100.0, latitude=48.1173, longitude=-1.6778, owner_id=owner.id)

    # Añadiendo una reseña usando place.id y owner.id
    review = Review(comment="Great stay!", rating=5, place_id=place.id, user_id=owner.id)
    place.add_review(review)

    assert place.title == "Apartamento en Rennes"
    assert place.price == 100.0
    assert place.owner_id == owner.id
    assert len(place.reviews) == 1
    assert place.reviews[0].comment == "Great stay!"
    print("✅ Place creation and relationship test passed!")

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi", description="Alta velocidad")
    assert amenity.name == "Wi-Fi"
    assert amenity.description == "Alta velocidad"
    print("✅ Amenity creation test passed!")

if __name__ == "__main__":
    print("--- Iniciando pruebas de Modelos (Alineados con UML) ---")
    test_user_creation()
    test_place_creation()
    test_amenity_creation()
    print("--- Todas las pruebas pasaron con éxito ---")
