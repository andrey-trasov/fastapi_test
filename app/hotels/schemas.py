from typing import Dict

from pydantic import BaseModel



class SHotel(BaseModel):
    name: str
    location: str
    service: Dict  # JSON хранится как Dict
    rooms_qunantity: int
    image_id: int

    class Config:
        orm_mode = True

class SHotelGet(SHotel):
    id: int