from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", [
    (4,"2030-05-01","2030-05-15", 3, 200),
    (4,"2030-05-01","2030-05-15", 4, 200),
    (4,"2030-05-01","2030-05-15", 5, 200),
    (4,"2030-05-01","2030-05-15", 6, 200),
    (4,"2030-05-01","2030-05-15", 7, 200),
    (4,"2030-05-01","2030-05-15", 7, 409),
    (4,"2030-05-01","2030-05-15", 7, 409),
])
async def test_add_and_get_booking(room_id, date_from, date_to, booked_rooms, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == booked_rooms

@pytest.mark.parametrize("authenticated_ac", [
    {"email": "artem.sam@yandex.ru", "password": "123456"},
    {"email": "govnovoz228@gmail.com", "password": "123456"},
], indirect=True)
async def test_get_and_drop_booking(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")

    bookings = response.json()
    print(f"Всего бронирований = {len(bookings)}")

    for booking in bookings:
        print(f"Удаление бронирования №{booking['id']}")
        await authenticated_ac.delete(f"/bookings/{booking['id']}")

    response = await authenticated_ac.get("/bookings")
    print(f"Бронирований после удаления = {len(response.json())}")
    assert len(response.json()) == 0