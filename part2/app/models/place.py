from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id
        self.reviews = [] # List to store related reviews
        self.amenities = [] # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity_id):
        """Adds an amenity ID to the place"""
        self.amenities.append(amenity_id)

    def update_details(self, data):
        """Updates place details"""
        self.update(data)
