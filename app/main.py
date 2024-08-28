import os
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

import sentry_sdk

from app.adminpanel.auth import authentication_backend
from app.adminpanel.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import BASE_DIR, settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.importer.router import router as router_importer
from app.prometheus.router import router as router_prometheus
from app.logger import logger

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        # decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info("Redis connection established", extra={"host": settings.REDIS_HOST})
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_images)
app.include_router(router_pages)
app.include_router(router_importer)
app.include_router(router_prometheus)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)

instrumentator.instrument(app).expose(app, tags=["Метрики"])

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # response.headers["X-Process-Time"] = str(process_time)
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response


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

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)
    # 1) uvicorn app.main:app --port 8088 --reload  # this is alternative command in cmd-line from the project root directory

    # 2) Запуск приложений Celery и Flower в консоли (для текущей структуры проекта):
    # 2.1) celery -A app.tasks.celery_config:celery_app worker --loglevel=INFO --pool=solo
    # 2.2) celery -A app.tasks.celery_config:celery_app flower

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
