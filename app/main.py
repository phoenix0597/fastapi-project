import uvicorn
from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel

app = FastAPI()


class HotelSchema(BaseModel):
    address: str
    name: str
    stars: Optional[int]
    

class HotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            has_spa: Optional[bool] = None,
            stars: Optional[int] = Query(None, ge=1, le=5)
    ):
        self.location = location,
        self.date_from = date_from,
        self.date_to = date_to,
        self.has_spa = has_spa,
        self.stars = stars


@app.get("/hotels")
async def get_hotels(search_args: HotelsSearchArgs = Depends()):
    hotels = [
        {
            "address": "ул. Пушкина, д. Колотушкина, 1",
            "name": "Родина",
            "stars": 3,
        },
        {
            "address": "ул. Пушкина, д. Колотушкина, 2",
            "name": "Hayatt Hotel",
            "stars": 5,
        },
    ]
    return search_args  # "Bridge Resort Hotel 5 stars"


class BookingSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
async def add_booking(booking: BookingSchema):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)
    # uvicorn main:app --reload - alternative command in cmd from project root directory

# Так пишут тесты
# import requests
# url = "http://127.0.0.1:8000/hotels/1"
# response = requests.get(
#     url,
#     params={
#         "date_from": "2022-01-01",
#         "date_to": "2022-01-02"}
# )
#
# print(response.json())
