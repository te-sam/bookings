from datetime import date
from operator import or_
from sqlalchemy import and_, func, select
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        """
        WITH rooms_left AS (
            WITH booked_rooms AS (
                SELECT * FROM bookings
                WHERE
                (date_from >= '2023-05-15' AND date_from < '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            )
            SELECT hotels.rooms_quantity - COUNT(booked_rooms.room_id) AS rooms_left, rooms.hotel_id FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            JOIN hotels ON hotels.id = rooms.hotel_id 
            GROUP BY rooms.hotel_id, hotels.rooms_quantity
        )
        SELECT id, name, location, services, rooms_quantity, image_id, rooms_left
        FROM hotels
        JOIN rooms_left ON hotels.id = rooms_left.hotel_id
        WHERE location LIKE '%Алтай%'
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                or_ (
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from < date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from
                    )
                )
            ).cte("booked_rooms")

            rooms_left = select(
                (Hotels.rooms_quantity - func.count(booked_rooms.c.room_id)).label('rooms_left'), Rooms.hotel_id
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).join(
                    Hotels, Hotels.id == Rooms.hotel_id
                ).group_by(Rooms.hotel_id, Hotels.rooms_quantity
                ).cte("rooms_left")
            
            get_free_hotels = select(
                Hotels.id, Hotels.name, Hotels.location, Hotels.services, Hotels.rooms_quantity, Hotels.image_id, rooms_left.c.rooms_left
            ).select_from(Hotels
            ).join(rooms_left, Hotels.id == rooms_left.c.hotel_id
            ).where(Hotels.location.ilike(f'%{location}%'))

            
            print(get_free_hotels.compile(engine, compile_kwargs={"literal_binds": True}))

            free_hotels = await session.execute(get_free_hotels)
            result = free_hotels.mappings().all()
            # rooms_left: int = rooms_left.scalar()
            print(result)
            print(type)

            if len(list(result)) > 0:
                return result
            else:
                return None