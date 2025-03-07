from datetime import datetime

from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (IncorrectTokenFormatException,
                            TokenAbsentException, TokenExpiredException,
                            UserIsNotPresentException)
from app.users.dao import UserDAO
from fastapi import Depends, Request


def get_token(request: Request):
    """
    Извлечение токена из заголовка Authorization
    """
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    """
    Получение текущего пользователя из токена
    """
    try:
        # декодируем функцию
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")    #получаем время создания токена
    if (not expire) or (int(expire) < datetime.now().timestamp()):   #проверяем валидност времени
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.find_by_id(int(user_id))    #Возвращаем иди юзера или None
    if not user:
        raise UserIsNotPresentException
    return user
