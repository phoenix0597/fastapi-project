from fastapi import APIRouter
from app.bookings.dao import BookingDAO


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("/")                                      # 1) нет аннотации responce model (не валидируем ответ клиенту)
async def get_bookings():                             # 2) не формируем ответ для конкретного пользователя (нет фильтра)
    # async with async_session_maker() as session:    # 3) в эндпоинте находится взаимодействие с БД - это неправильно -
    #     query = select(Bookings)                    # в соответствии с архитектурным паттерном MVC заменить на:
    #     result = await session.execute(query)       # result = BookingServise.get_all_bookings()
    #     print(result.mappings().all())
    #     return result.mappings().all()              # return result
    result = await BookingDAO.find_all()
    # result = await BookingDAO.find_by_id(1)
    return result
