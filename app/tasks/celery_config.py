from celery import Celery
from app.config import settings

celery_app = Celery(
    "tasks",
    broker = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include = ["app.tasks.tasks"],
)

celery_app.conf.update(
    result_expires=86400,  # время жизни результата задач в секундах (24 часа)
    # параметр определяет, будут ли попытки повторного подключения к брокеру во время запуска (начиная с версии 6.0)
    # в текущей версии celery (5.4.0) такое поведение определяется параметром broker_connection_retry (True по умолчанию)
    # если не указать параметр, то при запуске выдается соответсвующее предупреждение
    broker_connection_retry_on_startup=True,
)

# Запуск приложения Celery в консоли (для текущей структуры проекта):
# celery -A app.tasks.celery_config:celery_app worker --loglevel=INFO --pool=solo