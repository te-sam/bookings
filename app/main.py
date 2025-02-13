from contextlib import asynccontextmanager
import time
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_img
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.importer.router import router as router_imports

from app.logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        logger.info("Request handling time", extra={
            "process_time": round(process_time, 4)
        })
        return response


app = FastAPI(lifespan=lifespan)

# Порядок сохранится в документации
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_img)
app.include_router(router_imports)

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    middleware=[
        Middleware(ProcessTimeMiddleware)
    ]
)

instrumentator = Instrumentator(
    should_group_status_codes=False,  # не группировать статусы ответа
    excluded_handlers=[".*admin.*", "/metrics"],  # не смотреть на /metrics и админку, тут аналитика не нужна
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)

app.mount("/static", StaticFiles(directory="app/static"), "static")

