from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    booking = relationship("Bookings", back_populates="user")    #ссылка на модель привязанную через ForeignKey

    def __str__(self):
        return f"User {self.email}"
