import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


#тест на ауттентификацию
@pytest.mark.asyncio
@pytest.mark.parametrize("room_id, date_from, date_to, status_code",[
    (1, "2025-06-12", "2025-07-12", 200),
])
async def test_add_and_get_boocking(room_id, date_from, date_to, status_code):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/bookings/create", json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        })
        assert response.status_code == status_code

# #тест на ауттентификацию
# @pytest.mark.asyncio
# @pytest.mark.parametrize("user_id, room_id, date_from, date_to, status_code",[
#     (1, 1, "2025-06-12", "2025-07-12", 200),
# ])
# async def test_add_and_get_boocking(user_id, room_id, date_from, date_to, status_code):
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
#         response = await ac.post("/bookings/create", json={
#             "user_id": user_id,
#             "room_id": room_id,
#             "date_from": date_from,
#             "date_to": date_to,
#         })
#         assert response.status_code == status_code
