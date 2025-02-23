from datetime import date
from fastapi import FastAPI, Query, Depends
from typing import Optional

from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

from app.images.router import router as router_images

app = FastAPI()

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)

app.include_router(router_images)


# class SHotelsSearchArgs:
#    def __init__(
#        self,
#        location: str,
#        date_from: date,
#        date_to: date,
#        has_spa: Optional[bool] = None,  # не обязательный аргумент
#        stars: Optional[int] = Query(None, ge=1, le=5),    # не обязательный аргумент, может быть не меньше 1 и не больше 5
#    ):
#        self.location = location
#        self.date_from = date_from
#        self.date_to = date_to
#        self.has_spa = has_spa
#        self.stars = stars
#
#
# @app.get("/hotels")
# def get_hotels(
#        search_args: SHotelsSearchArgs = Depends()
# ):
#    return search_args
#
#
# class SBooking(BaseModel):
#     room_id: int
#     date_from: date
#     date_to: date
#
#
# @app.post("/bookings")
# def add_bookings(booking: SBooking):
#     pass


