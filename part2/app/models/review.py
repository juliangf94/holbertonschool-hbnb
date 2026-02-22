from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, comment, rating, place_id, user_id):
        super().__init__()
        self.comment = comment
        self.place_id = place_id
        self.user_id = user_id
        
        self.validate_rating(rating)
        self.rating = rating

    def validate_rating(self, rating):
        """Validates that rating is between 1 and 5"""
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
