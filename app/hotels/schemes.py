from typing import Optional
from pydantic import BaseModel


class HotelSchema(BaseModel):
    address: str
    name: str
    stars: Optional[int]