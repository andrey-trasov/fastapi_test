from datetime import date

from pydantic.v1 import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user))  -> list[SBooking]:
    """
    получение всех бронирований текущего пользователя
    """
    return await BookingDAO.find_all(user_id=user.id)

@router.post("/create")
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    """
    добавление нового бронирования
    """
    bookings = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not bookings:
        raise RoomCannotBeBooked
    send_booking_confirmation_email.delay(user.email)
