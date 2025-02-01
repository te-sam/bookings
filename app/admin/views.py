from sqladmin import ModelView

from app.users.models import Users
from app.bookings.models import Bookings


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"  # название строки
    name_plural = "Пользователи"  # название таблицы
    icon = "fa-solid fa-user"  # иконка для названия


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]
    can_delete = False
    name = "Бронирование"  # название строки
    name_plural = "Бронирования"  # название таблицы