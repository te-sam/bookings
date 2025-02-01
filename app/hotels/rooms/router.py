from datetime import date
from fastapi import APIRouter
from app.hotels.rooms.dao import RoomDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms_in_hotel(
    hotel_id: int,
	date_from: date,
	date_to: date, 
):
    return await RoomDAO.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)