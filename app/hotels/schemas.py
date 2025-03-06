from typing import Dict

from pydantic import ConfigDict, BaseModel



class SHotel(BaseModel):
    name: str
    location: str
    service: Dict  # JSON хранится как Dict
    rooms_qunantity: int
    image_id: int
    model_config = ConfigDict(from_attributes=True)

class SHotelGet(SHotel):
    id: int