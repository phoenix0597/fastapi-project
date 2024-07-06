from fastapi import APIRouter, Request, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import BookingSchema
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("/")  # , response_model=List[BookingSchema], response_model=list[BookingSchema])
async def get_bookings(user: Users = Depends(get_current_user)):
    print(user, type(user), user.id, user.email)
    result = await BookingDAO.find_all(user_id=user.id)
    return result
    # return user
