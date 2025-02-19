from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    id: int
    email: str
    hashed_password: str

    class Config:
        orm_mode = True

class SUserRegister(BaseModel):
    email: EmailStr
    hashed_password: str
