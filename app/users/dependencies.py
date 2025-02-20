from datetime import datetime

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from app.config import settings
from app.users.dao import UserDAO


def get_token(request: Request):
    """
    Извлечение токена из заголовка Authorization
    """
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: str = payload.get("exp")    #получаем время создания токена
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):   #проверяем валидност времени
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UserDAO.find_by_id(int(user_id))    #Возвращаем иди юзера или None
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
