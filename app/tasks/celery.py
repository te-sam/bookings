from celery import Celery
from app.config import settings

celery = Celery(
    "tasks",  # Название
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",  # Брокер для хранения задач
    include=["app.tasks.tasks"]  # путь хранения задач
)