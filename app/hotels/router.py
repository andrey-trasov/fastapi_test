from fastapi import APIRouter

from app.exceptions import TheHotelIsNotRented
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelGet

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


@router.get("/hotels")
async def hotel_list() -> list[SHotelGet]:
    """
    Получение списка всех отелей
    """
    return await HotelDAO.find_all()


@router.get("/hotel/{id}")
async def hotel_list(id: int) -> SHotelGet:
    """
    Получение списка всех отелей
    """
    hotel = await HotelDAO.find_one_or_none(id=id)
    if not hotel:
        raise TheHotelIsNotRented
    return hotel


@router.put("/hotel_update/{id}")
async def hotel_update(id: int, hotel_data: SHotel):
    """
    Обновление информации об отеле
    """
    hotel = await HotelDAO.update(id, hotel_data)
    if not hotel:
        raise TheHotelIsNotRented


@router.delete("/hotel_delete/{id}")
async def hotel_delete(id: int):
    """
    Удаление отеля по id
    """
    hotel = await HotelDAO.delete(id)
    if not hotel:
        raise TheHotelIsNotRented


