from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import BookingSchema
from app.exceptions import RoomCannotBeBookedException
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("/")  # , response_model=List[BookingSchema], response_model=list[BookingSchema])
async def get_bookings(user: Users = Depends(get_current_user)) -> list[BookingSchema]:
    print(user, type(user), user.id, user.email)
    result = await BookingDAO.find_all(user_id=user.id)
    return result
    # return user


@router.post("/")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    new_booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not new_booking:
        raise RoomCannotBeBookedException

    return {"message": "Successfully added booking"}
