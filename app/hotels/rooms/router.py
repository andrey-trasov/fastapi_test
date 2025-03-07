from app.exceptions import TheRoomIsNotRented
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoom, SRoomGet
from fastapi import APIRouter

router = APIRouter(
    prefix="/room",
    tags=["Комнаты"],
)


@router.post("/create")
async def room_create(room_data: SRoom):
    """
    Создание комнаты
    """
    await RoomDAO.add(hotel_id=room_data.hotel_id, name=room_data.name, description=room_data.description, price=room_data.price, services=room_data.services, quantity=room_data.quantity, image_id=room_data.image_id)


@router.get("/rooms")
async def room_list() -> list[SRoomGet]:
    """
    Получение списка всех комнат
    """
    return await RoomDAO.find_all()


@router.get("/room/{id}")
async def rooms_list(id: int) -> SRoomGet:
    """
    Получение списка всех комнат
    """
    room = await RoomDAO.find_one_or_none(id=id)
    if not room:
        raise TheRoomIsNotRented
    return room


@router.put("/room_update/{id}")
async def room_update(id: int, room_data: SRoom):
    """
    Обновление информации о комнате
    """
    room = await RoomDAO.update(id, room_data)
    if not room:
        raise TheRoomIsNotRented


@router.delete("/room_delete/{id}")
async def room_delete(id: int):
    """
    Удаление комнаты по id
    """
    room = await RoomDAO.delete(id)
    if not room:
        raise TheRoomIsNotRented
