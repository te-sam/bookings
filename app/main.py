from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Depends
from fastapi.staticfiles import StaticFiles
from typing import AsyncIterator
from app.admin.views import BookingsAdmin, UsersAdmin
from app.config import settings
from app.database import engine
from sqladmin import Admin
from app.admin.auth import authentication_backend

from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.users.models import Users
from app.users.router import router as router_users
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_img

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), "static")

#Поярядок сохранится в документации
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_img)


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
















# class SHotel(BaseModel):
#     addres: str
#     name: str
#     stars: int

# class HotelSearchArgs:
#     def __init__(
#         self,
#         location: str, #локация
#         date_from: date, #дата выезда
#         date_to: date, #дата въезда
#         stars: Optional[bool] = None,
#         has_spa: Optional[int] = Query(None, ge=1, le=5), #наличие спа
#     ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.stars = stars
#         self.has_spa = has_spa

# @app.get("/hotels", response_model=list[SHotel])
# def get_hotels(
#     searhc_args: HotelSearchArgs = Depends()
# ): 
#     hotels = [
#         {
#             "addres": "ул. Гагарина, 1а, Ярославль",
#             "name": "Общага",
#             "stars": 5,
#         }
#     ]
#     return hotels

# class SBooking(BaseModel):
#     room_id: int
#     date_from: date #дата выезда
#     date_to: date #дата въезда

# @app.post("/bookings")
# def add_booking(booking: SBooking):
#     pass

