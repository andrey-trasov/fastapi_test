from pydantic import BaseModel, ConfigDict, EmailStr


class SUser(BaseModel):
    id: int
    email: str
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

class SUserAuth(BaseModel):
    email: EmailStr
    hashed_password: str
