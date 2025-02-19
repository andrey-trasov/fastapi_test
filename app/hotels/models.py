from sqlalchemy import Column, Integer, String, JSON, ForeignKey

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    service = Column(JSON, nullable=False)
    rooms_qunantity = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)


class Rooms(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price= Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)
