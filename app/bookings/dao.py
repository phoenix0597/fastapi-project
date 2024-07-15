# DAO - Data Access Object / repo (repository) / service - названия, которые можно давать этому файлу
# это термины, отражающие названия паттерна, который реализует отделение БД от бизнес логики
from datetime import date

from sqlalchemy import or_, not_, func, select, insert, and_

from app.database import async_session_maker
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings
    
    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            NOT (date_to <= '2023-06-15' OR date_from >= '2023-06-20')
            )
        SELECT r.quantity - COUNT(br.room_id) FROM rooms r
        LEFT JOIN booked_rooms br ON r.id = br.room_id
        WHERE r.id = 1
        GROUP BY r.quantity
        """
        async with async_session_maker() as session:
            
            # Подзапрос с зарезервированными комнатами
            booked_rooms = select(Bookings).filter(
                Bookings.room_id == room_id,
                not_(or_(
                    Bookings.date_to <= date_from,
                    Bookings.date_from >= date_to
                ))
            ).subquery()
            
            # Основной запрос
            query = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('available_rooms')
            ).outerjoin(booked_rooms, Rooms.id == booked_rooms.c.room_id).filter(
                Rooms.id == room_id
            ).group_by(Rooms.quantity)
            
            result = await session.execute(query)
            print(result)
            available_rooms = result.scalar()
            print(f"{available_rooms=}")
            
            if available_rooms and available_rooms > 0:
                # Получаем цену за комнату
                get_price_query = select(Rooms.price).filter_by(id=room_id)
                price_result = await session.execute(get_price_query)
                price = price_result.scalar()
                
                add_booking_query = insert(Bookings).values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                new_booking = await session.execute(add_booking_query)
                await session.commit()
                return new_booking.scalar()
            
            else:
                print("Not enough rooms available")
                return None
