from fastapi import APIRouter

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel

router = APIRouter(
    prefix="/hotel",
    tags=["Отели"],
)

@router.post("/create")
async def hotel_create(hotel_data: SHotel):
    """
    Создание отеля
    """
    await HotelDAO.add(name=hotel_data.name, location=hotel_data.location, service=hotel_data.service, rooms_qunantity=hotel_data.rooms_qunantity, image_id=hotel_data.image_id)
