import os
from datetime import date, datetime

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.hotels.router import get_hotels_by_location_and_time

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))


@router.get("/hotels", response_class=HTMLResponse)
async def get_hotels_page(
        request: Request,
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date =  Query(..., description=f"Например, {datetime.now().date()} + 14 days"),
        hotels=Depends(get_hotels_by_location_and_time),
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={
            "request": request,
            "hotels": hotels,
            "location": location,
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
        },
    )
