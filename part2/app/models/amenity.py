from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
        self.name = name
        self.description = description
