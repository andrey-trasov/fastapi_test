from typing import Dict

from pydantic import BaseModel



class SRoom(BaseModel):
    hotel_id: int
    name: str
    description: str
    price: int
    services: Dict
    quantity: int
    image_id: int

    class Config:
        orm_mode = True

class SRoomGet(SRoom):
    id: int