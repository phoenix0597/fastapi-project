from typing import Optional
from pydantic import BaseModel


class HotelSchema(BaseModel):
    # address: str
    location: str  # Изменили address на location
    name: str
    stars: Optional[int] = None
    image_id: int
    rooms_left: int
    services: Optional[list[str]] = None
