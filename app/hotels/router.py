from datetime import date
from fastapi import APIRouter
from app.exceptions import HotelNotFoundError, LocationHotelsNotFoundError
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelOnly
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
@cache(expire=60)
async def get_hotels_by_location(
	location: str,
	date_from: date,
	date_to: date,
) -> list[SHotel]:
    hotels = await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)
    if not hotels:
        raise LocationHotelsNotFoundError
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotels_by_id(hotel_id: int) -> SHotelOnly:
    hotel = await HotelDAO.find_one_or_none(id=hotel_id)
    if not hotel:
        raise HotelNotFoundError
    return hotel