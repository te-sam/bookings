from datetime import date
from typing import List
from pydantic import BaseModel, ConfigDict

class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    # image_id: int
    # name: str
    # description: str
    # services: List[str]

    # "room_id": 6,
    # "user_id": 5,
    # "date_from": "2023-05-14",
    # "date_to": "2023-05-16",
    # "price": 9815,
    # "total_cost": 19630,
    # "total_days": 2,
    # "image_id": 12,
    # "name": "2-комнатный номер люкс комфорт",
    # "description": "Красивый номер для молодоженов.",
    # "services": []

    # model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes=False