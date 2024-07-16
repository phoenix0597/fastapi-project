from fastapi import UploadFile, APIRouter
import shutil
import os
from app.config import BASE_DIR

router = APIRouter(
    prefix="/imsges",
    tags=["Images download"],
)


@router.post("/hotels")
async def download_hotels_image(name: int, file: UploadFile):
    file_path = os.path.join(BASE_DIR, "app", "static", "images", f"{name}.webp")
    with open(file_path, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return {"message": "Image uploaded"}
