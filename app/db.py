from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

DATABASE_URL = 'sqlite:///./weather.db'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Создаёт таблицы в базе данных на основе моделей.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Зависимость FastAPI. Предоставляет сессию работы с БД.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
