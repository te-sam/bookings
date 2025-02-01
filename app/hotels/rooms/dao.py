from datetime import date
from operator import or_
from sqlalchemy import and_, func, select
from app.bookings.models import Bookings
from app.database import async_session_maker, engine
from app.hotels.rooms.models import Rooms
from app.dao.base import BaseDAO


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(
        cls,
        hotel_id: int,
        date_from: date,
	    date_to: date, 
    ):
        async with async_session_maker() as session:
            """
            WITH booked_rooms AS (
                SELECT room_id, SUM(total_cost) AS total_cost, COUNT(room_id) AS count_bookings
                FROM bookings
                WHERE 
                date_from >= '2023-06-24' AND date_from < '2023-06-30' 
                OR 
                date_from <= '2023-06-24' AND date_to > '2023-06-24'
                GROUP BY room_id
            )
            SELECT id, hotel_id, name, description, services, price, quantity, image_id, total_cost , quantity - count_bookings AS left_rooms
            FROM rooms
            JOIN booked_rooms ON booked_rooms.room_id = rooms.id 
            WHERE hotel_id = 1
            GROUP BY id, total_cost, count_bookings
            """
            booked_rooms = select(
                Bookings.room_id, 
                func.sum(Bookings.total_cost).label("total_cost"), 
                func.count(Bookings.room_id).label("count_bookings")
            ).select_from(Bookings
            ).where(
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
            ).group_by(Bookings.room_id
            ).cte("booked_rooms")

            get_rooms = select(
                Rooms.id, 
                Rooms.hotel_id, 
                Rooms.name, 
                Rooms.description, 
                Rooms.services, 
                Rooms.price, 
                Rooms.quantity, 
                Rooms.image_id,
                booked_rooms.c.total_cost, 
                (Rooms.quantity - booked_rooms.c.count_bookings).label("left_rooms")
            ).select_from(Rooms
            ).join(booked_rooms, booked_rooms.c.room_id == Rooms.id
            ).where(Rooms.hotel_id==hotel_id
            ).group_by(Rooms.id, booked_rooms.c.total_cost, booked_rooms.c.count_bookings)

            
            print(get_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

            list_rooms = await session.execute(get_rooms)
            result = list_rooms.mappings().all()
            # rooms_left: int = rooms_left.scalar()
            print(result)
            print(type)

            if len(list(result)) > 0:
                return result
            else:
                return None