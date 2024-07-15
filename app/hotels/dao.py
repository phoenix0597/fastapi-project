from datetime import date

from sqlalchemy import or_, func, not_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels
    
    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE
                NOT (date_to <= '2023-06-15' OR date_from >= '2023-06-20')
            GROUP BY room_id
        ),
        booked_hotels AS (
            SELECT hotel_id, SUM(rooms.quantity - COALESCE(rooms_booked, 0)) AS rooms_left
            FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            GROUP BY hotel_id
        )
        SELECT * FROM hotels
        LEFT JOIN booked_hotels ON booked_hotels.hotel_id = hotels.id
        WHERE rooms_left > 0 AND location LIKE '%Алтай%';
        """
        # Запрос к БД, который подсчитывает количество забронированных комнат в заданный период
        booked_rooms = (
            select(
                Bookings.room_id,
                func.count(Bookings.room_id).label('rooms_booked')
            ).where(
                not_(or_(
                    Bookings.date_to <= date_from,
                    Bookings.date_from >= date_to
                ))
            ).group_by(Bookings.room_id).cte('booked_rooms')
        )
        
        # Запрос к БД, который подсчитывает количество свободных комнат в каждом отеле
        booked_hotels = (
            select(
                Rooms.hotel_id,
                func.sum(Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label('rooms_left')
            )
            .select_from(Rooms)
            .outerjoin(booked_rooms, booked_rooms.c.room_id == Rooms.id)
            .group_by(Rooms.hotel_id)
            .cte('booked_hotels')
        )
        # Запрос к БД, выбирает отели, которые имеют свободные комнаты и находятся в локации "Алтай"
        hotels_query = (
            select(Hotels, booked_hotels.c.rooms_left)
            .outerjoin(booked_hotels, booked_hotels.c.hotel_id == Hotels.id)
            .where(booked_hotels.c.rooms_left > 0)
            .where(Hotels.location.like(f"%{location}%"))
        )
        
        async with async_session_maker() as session:
            result = await session.execute(hotels_query)
            hotels_list = result.mappings().all()
            
            # Преобразуем данные
            formatted_hotels = [
                {'name': hotel['Hotels'].name, 'location': hotel['Hotels'].location} for hotel in hotels_list
            ]
            
            # Выводим для отладки
            for hotel in formatted_hotels:
                print(f"Hotel Name: {hotel['name']}, Location: {hotel['location']}")
            
            return formatted_hotels
        