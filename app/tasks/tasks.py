from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_config import celery_app
from PIL import Image
from pathlib import Path
import smtplib
from time import sleep

from app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def process_pic(
        path: str,

):
    image_path = Path(path)
    image = Image.open(image_path)
    resized_image_1024_768 = image.resize((1024, 768))
    resized_image_200_150 = image.resize((200, 150))
    resized_image_1024_768.save(f"app/static/images/1024_768{image_path.name}")
    resized_image_200_150.save(f"app/static/images/200_150{image_path.name}")


@celery_app.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):

    sleep(10)
    email_to_mock = settings.SMTP_USER  # для проверки отправляю письмо самому себе
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)

# ---------------------------
# запуск celery в консоли:
# celery -A app.tasks.celery_config:celery_app worker --loglevel=INFO --pool=solo
# ---------------------------
# запуск flower в консоли:
# celery -A app.tasks.celery_config:celery_app flower
