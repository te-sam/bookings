from fastapi import HTTPException, status


class BookingException(HTTPException):  # <-- наследуемся от HTTPException,который наследован от Exception
    status_code = 500 # <-- задаем значения по умолчанию detail
    def  __init__ (self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(BookingException):  # обязательно наследуемся от нашего класса
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class IncorrectEmailPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"

class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен истек"

class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"

class IncorrectTokenForatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"

class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED

class RoomCannotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Не осталось свободных номеров"

class BookingNotFoundError(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Такого заказа не существует"

class HotelNotFoundError(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Такого отеля не существует"

class HotelNotFoundError(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Такого отеля не существует"

class LocationHotelsNotFoundError(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="По такой локации отели не найдены"

class DateFromAfterDateTo(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Дата заезда позже даты выезда"

class DateRangeLimitExceeded(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Бронирование на срок больше 30 дней невозможно"

class CannotAddDataToDatabase(BookingException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось добавить запись"

class CannotProcessCSV(BookingException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось обработать CSV файл"