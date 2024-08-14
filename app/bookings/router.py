from datetime import date, timedelta

from fastapi import APIRouter, Depends, status, BackgroundTasks
from pydantic import TypeAdapter
# from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import BookingSchema
from app.exceptions import (RoomCannotBeBookedException, CannotBookHotelForLongPeriodException,
                            CannotBookHotelBeforeTodayException, DateFromCannotBeAfterDateToException)
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.tasks.tasks import send_booking_confirmation_email

# Создаем TypeAdapter для схемы BookingSchema
booking_schema_adapter = TypeAdapter(BookingSchema)

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[BookingSchema]:
    print(user, type(user), user.id, user.email)
    result = await BookingDAO.find_all(user_id=user.id)
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    if date_from >= date_to:
        status_code = status.HTTP_400_BAD_REQUEST
        raise DateFromCannotBeAfterDateToException
    elif date_from < date.today():
        status_code = status.HTTP_400_BAD_REQUEST
        raise CannotBookHotelBeforeTodayException
    elif date_to - date_from > timedelta(days=30):
        status_code = status.HTTP_400_BAD_REQUEST
        raise CannotBookHotelForLongPeriodException
    elif date_to - date_from < timedelta(days=30):

        new_booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
        if not new_booking:
            raise RoomCannotBeBookedException

        # booking_dict = parse_obj_as(BookingSchema, new_booking).dict()
        # Преобразуйте объект Bookings в словарь
        booking_dict = {
            "id": new_booking.id,
            "room_id": new_booking.room_id,
            "user_id": new_booking.user_id,
            "date_from": new_booking.date_from,
            "date_to": new_booking.date_to,
            "price": new_booking.price,
            "total_cost": new_booking.total_cost,
            "total_days": new_booking.total_days,
        }

        # Используем TypeAdapter для валидации данных
        validated_booking = booking_schema_adapter.validate_python(booking_dict)

        # If we use Celery to send confirmation email:
        send_booking_confirmation_email.delay(validated_booking.model_dump(), user.email)

        # If we use embedded in FastAPI BackgroundTasks to send confirmation email:
        # background_tasks = BackgroundTasks()
        # background_tasks.add_task(send_booking_confirmation_email, validated_booking.model_dump(), user.email)

    return validated_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.delete(id=booking_id, user_id=user.id)
