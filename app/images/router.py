import os
import shutil

from fastapi import APIRouter, UploadFile

from app.config import BASE_DIR
from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Images download"],
)


@router.post("/hotels")
async def download_hotels_image(name: int, file: UploadFile):
    file_path = os.path.join(BASE_DIR, "app", "static", "images", f"{name}.webp")
    # print(type(f"{file_path=}"))
    with open(file_path, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(file_path)

    return {"message": "Image uploaded"}
