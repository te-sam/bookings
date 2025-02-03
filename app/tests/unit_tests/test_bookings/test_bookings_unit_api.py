from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (3, '2023-06-01', '2023-06-20', 200),
    (3, '2025-03-01', '2025-03-31', 200),
    (3, '2025-03-01', '2025-04-01', 400),
    (2, '2025-04-01', '2025-03-01', 400),
])
async def test_add(room_id, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code