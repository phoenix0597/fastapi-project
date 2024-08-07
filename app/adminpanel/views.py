from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.booking]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    category = "АККАУНТЫ"
    column_details_list = [Users.id, Users.email]
    # column_formatters_detail = {Users.email: lambda m, a: m.email[:10]}

    page_size = 50
    page_size_options = [25, 50, 100, 200]

class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]
    # can_delete = False
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-money-bill"
    category = "ОТЕЛИ"
    column_details_list = [Bookings.id, Bookings.user_id, Bookings.room_id, Bookings.price, Bookings.total_cost, Bookings.total_days, Bookings.date_from, Bookings.date_to]
    # column_formatters_detail = {Users.email: lambda m, a: m.email[:10]}

    page_size = 50
    page_size_options = [25, 50, 100, 200]


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.room]
    # can_delete = False
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"
    category = "ОТЕЛИ"
    page_size_options = [25, 50, 100, 200]


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.booking]
    # can_delete = False
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"
    category = "ОТЕЛИ"
    # column_formatters_detail = {Users.email: lambda m, a: m.email[:10]}

    page_size = 50
    page_size_options = [25, 50, 100, 200]
