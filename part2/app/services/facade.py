from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()


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
        owner = self.user_repo.get(User, place_data['owner_id'])
        if owner is None:
            raise ValueError("Owner not found")

        # Amenities check (if exists)
        amenities = []
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(Amenity, amenity_id)
                if amenity is None:
                    raise ValueError(f"Amenity not found: {amenity_id}")
                amenities.append(amenity)

        # Create place
        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )

        # Add amenities
        place.amenities = amenities

        # Save place
        self.place_repo.new(place)
        self.place_repo.save()

        return place


    def get_place(self, place_id):
        # Get place
        place = self.place_repo.get(Place, place_id)
        if place is None:
            return None

        # Get owner
        owner = self.user_repo.get(User, place.owner_id)
        place.owner = owner

        # Get amenities
        amenities = []
        for amenity in place.amenities:
            if isinstance(amenity, str):
                amenity_obj = self.amenity_repo.get(Amenity, amenity)
                if amenity_obj:
                    amenities.append(amenity_obj)
            else:
                amenities.append(amenity)

        place.amenities = amenities
        return place


    def get_all_places(self):
        places = self.place_repo.all(Place)
        result = []

        for place in places:
            owner = self.user_repo.get(User, place.owner_id)
            place.owner = owner

            amenities = []
            for amenity in place.amenities:
                if isinstance(amenity, str):
                    amenity_obj = self.amenity_repo.get(Amenity, amenity)
                    if amenity_obj:
                        amenities.append(amenity_obj)
                    else:
                        amenities.append(amenity)
            place.amenities = amenities
            result.append(place)
        return result


    def update_place(self, place_id, place_data):
        # Get original place
        place = self.place_repo.get(Place, place_id)
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
                        amenity = self.amenity_repo.get(Amenity, amenity_id)
                        if amenity is None:
                            raise ValueError(f"Amenity not found: {amenity_id}")
                        amenities_list.append(amenity)
                    place.amenities = amenities_list
                else:
                    setattr(place, field, value)

        # Save updated place
        self.place_repo.save()
        return place
