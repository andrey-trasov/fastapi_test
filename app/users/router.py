from fastapi import APIRouter, HTTPException

from app.users.auth import get_password_hash
from app.users.dao import UserDAO
from app.users.schemas import SUser, SUserRegister

from typing import List

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)

@router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)    #проверяем есть ли такой пользователь в бд
    if existing_user:    #если есть
        raise HTTPException(status_code=400)    #выдаем ошибку
    hashed_password = get_password_hash(user_data.hashed_password)    #хешируем пароль
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
















@router.get("")
async def get_users() -> list[SUser]:
    return await UserDAO.find_all()
