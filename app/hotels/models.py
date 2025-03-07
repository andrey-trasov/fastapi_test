from sqlalchemy import JSON, Column, Integer, String

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    service = Column(JSON, nullable=False)
    rooms_qunantity = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)

