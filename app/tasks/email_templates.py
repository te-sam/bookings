from email.message import EmailMessage
from app.config import settings
from pydantic import EmailStr


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"  # Тема письма
    email["From"] = settings.SMTP_USER  # От кого отправляем
    email["To"] = email_to  # Кому отправляем

    email.set_content(  # само сообщение
        f"""
            <h1>Подтвердите бронирование</h1>
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}
        """,
        subtype="html"
    )
    return email