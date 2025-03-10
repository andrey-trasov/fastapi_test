from typing import List

from app.exceptions import IncorrectEmailOrPassword, UserAlreadyExistsException
from app.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUser, SUserAuth
from fastapi import APIRouter, Depends, HTTPException, Response, status

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    """
    регистрация пользователя

    """
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)    #проверяем есть ли такой пользователь в бд
    if existing_user:    #если есть
        raise UserAlreadyExistsException    #выдаем ошибку
    hashed_password = get_password_hash(user_data.hashed_password)    #хешируем пароль
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    """
    автоизация пользователя

    """
    user = await authenticate_user(user_data.email, user_data.hashed_password)
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    """
    выход пользователя из системы

    """
    response.delete_cookie("booking_access_token",)

@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    """
    получение информации о текущем пользователе

    """
    return current_user







# @router.get("")
# async def get_users() -> list[SUser]:
#     return await UserDAO.find_all()
