import os
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.config import settings
from app.hotels.router import get_hotels_by_location_and_time

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))


def get_default_dates():
    today = datetime.now().date()
    date_from_default = today + timedelta(days=2)
    date_to_default = today + timedelta(days=12)
    return date_from_default, date_to_default


@router.get("/hotels", response_class=HTMLResponse)
async def get_hotels_page(
        request: Request,
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()} + 2 days"),
        date_to: date =  Query(..., description=f"Например, {datetime.now().date()} + 12 days"),
        hotels=Depends(get_hotels_by_location_and_time),
):
    dates: tuple[date, date] = Depends(get_default_dates),
    return templates.TemplateResponse(
        name="hotels.html",
        context={
            "request": request,
            "hotels": hotels,
            "location": location,
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "host_ip": settings.HOST_IP,
        },
    )
