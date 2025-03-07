from http import client

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

#тес длля 1 запроса

# @pytest.mark.asyncio
# async def test_register_user():
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
#         response = await ac.post("/user/register", json={
#             "email": "tests@example.com",
#             "hashed_password": "test123",
#         })
#
#         assert response.status_code == 200

# пишем 1 тест, с разными данными
#тест на регистраци
@pytest.mark.asyncio
@pytest.mark.parametrize("email, password, status_code",[
    ("kot@pes.com", "12345",  200),    #проверка регстрации
    ("kot2@pes.com", "12345",  200),    #проверка регстрации
    ("kot3@pes.com", "12345",  200),    #проверка регстрации
    ("kot3@pes.com", "12345",  409),    #проверка регистрации с существующим email
    ("kot", "12345",  422),    #проверка на регистацию без email
])
async def test_register_user(email, password, status_code):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/user/register", json={
            "email": email,
            "hashed_password": password,
        })

        assert response.status_code == status_code

#тест на ауттентификацию
@pytest.mark.asyncio
@pytest.mark.parametrize("email, password, status_code",[
    ("a@mail.ru", "12345",  200),    #проверка на авторизацию
    ("yui", "ergerer", 422),    #проверка на авторизацию с ошибкой
])
async def test_login_user(email, password, status_code):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/user/login", json={
            "email": email,
            "hashed_password": password,
        })

        assert response.status_code == status_code


# @pytest.mark.asyncio
# @pytest.mark.parametrize("hotel_id, name, description, price, services, quantity, image_id, status_code",[
#     (1, "Номер на 2", "Комфортнй номер", 1000, {"dinner": "Yes"}, 10, 10, 200),    #проверка регстрации
#
# ])
# async def test_create_rooms(hotel_id, name, description, price, services, quantity, image_id, status_code):
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
#         response = await ac.post("/room/create", json={
#             "hotel_id": hotel_id,
#             "name": name,
#             "description": description,
#             "price": price,
#             "services": services,
#             "quantity": quantity,
#             "image_id": image_id,
#         })
#
#         assert response.status_code == status_code