import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.adminpanel.auth import authentication_backend
from app.adminpanel.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import BASE_DIR, settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users

# from fastapi_cache.decorator import cache





# print(BASE_DIR)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        # decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")), name="static")
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Coookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)
    # uvicorn app.main:app --port 8088 --reload  # this is alternative command in cmd from project root directory

    # Запуск приложений Celery и Flower в консоли (для текущей структуры проекта):
    # celery -A app.tasks.celery_config:celery_app worker --loglevel=INFO --pool=solo
    # celery -A app.tasks.celery_config:celery_app flower

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
