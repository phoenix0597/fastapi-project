from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms
    
    @classmethod
    async def find_all(cls, hotel_id: int):
        pass