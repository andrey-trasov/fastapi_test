import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseModel
from redis import asyncio as aioredis
from fastapi import Request
from sqladmin import Admin, ModelView
from starlette.staticfiles import StaticFiles
from fastapi_versioning import VersionedFastAPI


from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.users.router import router as router_users
from fastapi import Depends, FastAPI, Query
from app.logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield





app = FastAPI(lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)

app.include_router(router_images)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],
)

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    # description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request handling time", extra={'process_time': round(process_time, 4)})
    return response











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


