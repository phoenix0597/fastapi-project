from pydantic import BaseModel
from datetime import date


class BookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    
    class Config:
        # orm_mode = True  # Используйте 'from_attributes' вместо 'orm_mode'
        from_attributes = True  # Используйте 'from_attributes' вместо 'orm_mode'7
