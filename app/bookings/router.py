from datetime import date, timedelta
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_versioning import version
from pydantic import TypeAdapter
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import BookingNotFoundError, DateFromAfterDateTo, DateRangeLimitExceeded, RoomCannotBeBooked

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("/{booking_id}")
@version(2)
async def get_booking_by_id(booking_id: int) -> SBooking:
    booking = await BookingDAO.find_by_id(booking_id)
    if not booking:
        raise BookingNotFoundError
    return booking


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    bookings = await BookingDAO.find_all(user_id=user.id)
    return bookings if bookings else []


@router.post("")
async def add_booking(
    room_id: int, 
    date_from: date, 
    date_to: date,
    user: Users = Depends(get_current_user),
):
    if date_from >= date_to:
        raise DateFromAfterDateTo
    
    if date_to - date_from > timedelta(days=30):
        raise DateRangeLimitExceeded
    
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    
    # booking_dict = SBooking(**booking.__dict__).model_dump()
    booking_dict = TypeAdapter(SBooking).validate_python(booking, from_attributes=True).model_dump()
    print(type(booking_dict))
    #send_booking_confirmation_email.delay(booking_dict, user.email)  # Отправить сообщение
    return booking
    

@router.delete("/{booking_id}")
async def drop_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.drop(user.id, booking_id)
    if not booking:
        raise BookingNotFoundError
    return JSONResponse(content=None,status_code=204)