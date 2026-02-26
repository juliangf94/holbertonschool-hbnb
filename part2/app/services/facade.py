#!/usr/bin/python3

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    """
    Facade layer that connects the API (Presentation layer)
    to the Business Logic and Persistence layers.
    """

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
    
    # ==========================================
    # PLACES CRUD
    # ==========================================
    def create_place(self, place_data):
        # Field requirements
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"Missing required field: {field}")

        # Price validation
        if place_data['price'] < 0:
            raise ValueError("Price must be greater than or equal to 0")

        # Latitude validation
        if not (-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        # Longitude validation
        if not (-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        # Owner exists?
        owner = self.user_repo.get(place_data['owner_id'])
        if owner is None:
            raise ValueError("Owner not found")

        # Create place
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ""),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )

        # Amenities check (if exists)
        amenities = []
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                # InMemoryRepository.get() only accepts obj_id since each entity uses its own repository instance.
                amenity = self.amenity_repo.get(amenity_id)
                if amenity is None:
                    raise ValueError(f"Amenity not found: {amenity_id}")
                amenities.append(amenity)

        # Add amenities
        place.amenities = amenities

        # Save place
        """self.place_repo.new(place)
        self.place_repo.save()"""
        # we use our method add
        self.place_repo.add(place)
        owner.places.append(place)

        return place


    def get_place(self, place_id):
        # Get place
        place = self.place_repo.get(place_id)
        if place is None:
            return None

        # Get owner
        owner = self.user_repo.get(place.owner_id)
        place.owner = owner

        # Get amenities
        amenities = []
        for amenity in place.amenities:
            if isinstance(amenity, str):
                amenity_obj = self.amenity_repo.get(amenity)
                if amenity_obj:
                    amenities.append(amenity_obj)
            else:
                amenities.append(amenity)

        place.amenities = amenities
        return place


    def get_all_places(self):
        places = self.place_repo.get_all()
        result = []

        for place in places:
            owner = self.user_repo.get(place.owner_id)
            place.owner = owner

            amenities = []
            for amenity in place.amenities:
                if isinstance(amenity, str):
                    amenity_obj = self.amenity_repo.get(amenity)
                    if amenity_obj:
                        amenities.append(amenity_obj)
                    else:
                        amenities.append(amenity)
            place.amenities = amenities
            result.append(place)
        return result


    def update_place(self, place_id, place_data):
        # Get original place
        place = self.place_repo.get(place_id)
        if place is None:
            return None

        # Updating fields
        updatable_fields = ['title', 'description', 'price', 'latitude',
                            'longitude', 'amenities']

        for field in updatable_fields:
            if field in place_data:
                value = place_data[field]

                # Validation of fields
                if field == 'price' and value < 0:
                    raise ValueError("Price must be >= 0")
                if field == 'latitude' and not (-90 <= value <= 90):
                    raise ValueError("Latitude must be between -90 and 90")
                if field == 'longitude' and not (-180 <= value <= 180):
                    raise ValueError("Longitude must be between -180 and 180")

                # Verify amenities
                if field == 'amenities':
                    amenities_list = []
                    for amenity_id in value:
                        amenity = self.amenity_repo.get(amenity_id)
                        if amenity is None:
                            raise ValueError(f"Amenity not found: {amenity_id}")
                        amenities_list.append(amenity)
                    place.amenities = amenities_list
                else:
                    setattr(place, field, value)

        """# Save updated place
        self.place_repo.save()"""
        return place
    # -------------------------
    # USERS CRUD
    # -------------------------
    # Create
    def create_user(self, user_data):
        """
        Create a new user and store it in the repository.
        """
        # Collects all errors
        errors = []

        if self.get_user_by_email(user_data.get('email')):
            errors.append("Email already registered")

        user = None
        try:
            # We create the user object
            user = User(**user_data)
        except ValueError as e:
            errors.append(str(e))

        # Separate errors with ", "
        if errors:
            raise ValueError(", ".join(errors))

        # We save it in the database
        self.user_repo.add(user)
        return user

    # -------------------------
    # READ (single user)
    # -------------------------
    def get_user(self, user_id):
        """
        Retrieve a user by ID.
        """
        return self.user_repo.get(user_id)

    # -------------------------
    # READ (by email)
    # -------------------------
    def get_user_by_email(self, email):
        """
        Retrieve a user by email.
        """
        return self.user_repo.get_by_attribute('email', email)

    # -------------------------
    # READ (all users)
    # -------------------------
    def get_all_users(self):
        """
        Retrieve all users.
        """
        return self.user_repo.get_all()

    # -------------------------
    # UPDATE
    # -------------------------
    def update_user(self, user_id, user_data):
        """
        Update an existing user.
        Returns None if user does not exist.
        Raises ValueError if email already exists.
        """
        user = self.user_repo.get(user_id)

        if not user:
            return None

        # Check email uniqueness if modified
        if "email" in user_data:
            existing_user = self.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")
        # The update operation must be outside the email condition block 
        # to ensure other attributes (like first_name) are still updated even if no email is provided.
        updated_user = self.user_repo.update(user_id, user_data)
        return updated_user

    # -------------------------
    # AMENITY CRUD
    # -------------------------
    def create_amenity(self, amenity_data):
        # Create a new amenity and check for duplication
        if "name" not in amenity_data or not amenity_data["name"].strip():
            raise ValueError("Amenity must have a non-empty name")

        # Check if the amenity already exists by name
        existing = self.amenity_repo.get_by_attribute("name", amenity_data["name"])
        if existing:
            raise ValueError("Amenity with this name already exists")

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        # Check for duplication if the name is changed
        if "name" in amenity_data:
            existing = self.amenity_repo.get_by_attribute("name", amenity_data["name"])
            if existing and existing.id != amenity_id:
                raise ValueError("Amenity with this name already exists")

        updated_amenity = self.amenity_repo.update(amenity_id, amenity_data)
        return updated_amenity

    # -------------------------
    # REVIEW CRUD
    # -------------------------

    