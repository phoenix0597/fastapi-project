# DAO - Data Access Object / repo (repository) / service - названия, которые можно даваать этому файлу
# это термины, отражающие названия паттерна, который реализует отделение БД от бизнес логики
from sqlalchemy import select

from app.database import async_session_maker
from app.bookings.models import Bookings
from app.dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings