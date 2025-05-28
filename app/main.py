from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import init_db
from .endpoints import router as weather_router
from .endpoints import autocomplete_router

templates = Jinja2Templates(directory='app/templates')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Обработчик жизненного цикла приложения: инициализация БД.
    """
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(
    directory='app/templates/static'),
    name='static'
)
app.include_router(weather_router)
app.include_router(autocomplete_router)
