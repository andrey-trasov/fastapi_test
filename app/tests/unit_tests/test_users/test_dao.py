from app.users.dao import UserDAO
import pytest


#проверка функции которая достает пользовтелей по id
@pytest.mark.asyncio
async def test_find_user_by_id():
    user = await UserDAO.find_by_id(1)
    assert user.id == 1
    assert user.email == "a@mail.ru"


#проверка функции коорая достает пользовтелей по id
@pytest.mark.asyncio
@pytest.mark.parametrize("user_id, email, exists",[
    (1, "a@mail.ru", True),    #проверка пользователя
    (100, "...", False),    #проверка пользователя с ошибкой
])
async def test_find_user_by_id(user_id, email, exists):
    user = await UserDAO.find_by_id(user_id)
    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
