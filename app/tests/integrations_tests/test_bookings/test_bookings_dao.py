import pytest

from app.bookings.dao import BookingDAO
from datetime import datetime


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
            user_id=1,
            room_id=2,
            date_from=datetime.strptime("2023-07-14", "%Y-%m-%d"),
            date_to=datetime.strptime("2023-07-29", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 1
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None


async def test_add_get_and_drop_booking():
    new_booking = await BookingDAO.add(
            user_id=4,
            room_id=3,
            date_from=datetime.strptime("2025-07-14", "%Y-%m-%d"),
            date_to=datetime.strptime("2025-08-02", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 4
    assert new_booking.room_id == 3

    new_booking = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None

    await BookingDAO.drop(new_booking.user_id, new_booking.id)
    
    droped_booking = await BookingDAO.find_by_id(new_booking.id)
    assert droped_booking is None
        

