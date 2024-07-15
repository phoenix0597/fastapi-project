import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)


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
