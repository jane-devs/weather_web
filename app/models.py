from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)


class Search(Base):
    __tablename__ = 'searches'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    city = Column(String)
    city_en = Column(String)
    timestamp = Column(DateTime, default=datetime.now)


def get_or_create_user(db, user_id):
    """
    Возвращает пользователя по ID или создаёт нового.
    """
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        user = User(id=user_id)
        db.add(user)
        db.commit()
    return user


def add_search_entry(db, user_id, city):
    """
    Добавляет запись поиска города.
    """
    search = Search(user_id=user_id, city=city)
    db.add(search)
    db.commit()


def get_search_stats(db):
    """
    Возвращает статистику количества запросов по каждому городу.
    """
    from sqlalchemy import func
    return dict(db.query(
        Search.city, func.count()).group_by(Search.city).all())
