from typing import Dict

from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    hotel_id: int
    name: str
    description: str
    price: int
    services: Dict
    quantity: int
    image_id: int
    model_config = ConfigDict(from_attributes=True)

class SRoomGet(SRoom):
    id: int