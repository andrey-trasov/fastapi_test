from fastapi import APIRouter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@router.get("")
async def get_bookings() -> list[SBooking]:
    return await BookingDAO.find_all()





# @router.get("/{bookings_id}")
# def get_bookings2(bookings_id):
#     pass
