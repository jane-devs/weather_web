from collections import Counter
from datetime import datetime
import json
from urllib.parse import quote

from fastapi import (
    APIRouter, Request, Form, Response, Depends, Query, status
)
from fastapi.responses import (
    HTMLResponse, RedirectResponse, JSONResponse
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from .weather import fetch_weather
from .db import get_db
from .models import Search
from .services import translate

templates = Jinja2Templates(directory='app/templates')

router = APIRouter()
autocomplete_router = APIRouter()
city_counter = Counter()
city_stats = {}


@autocomplete_router.get(
    '/api/autocomplete',
    response_model=list[str]
)
def autocomplete(
    query: str = Query(..., description='Префикс названия города'),
    db: Session = Depends(get_db)
):
    """
    Возвращает список городов, начинающихся с заданного префикса.

    Извлекает уникальные названия городов из базы данных и
    фильтрует по введённому префиксу.
    """
    results = db.query(Search.city).distinct().all()
    all_cities = [row[0] for row in results]
    matches = [c for c in all_cities if c.lower().startswith(query.lower())]
    return matches


@autocomplete_router.get('/api/get-city-stats')
def get_city_stats(
    page: int = Query(1, ge=1, description='Номер страницы'),
    limit: int = Query(
        10, ge=1, le=100, description='Количество элементов на странице'),
    db: Session = Depends(get_db)
):
    """
    Возвращает статистику по городам — количество запросов на каждый город.

    Данные пагинируются.
    """
    offset = (page - 1) * limit
    query = (
        db.query(Search.city, func.count(Search.city).label('count'))
        .group_by(Search.city)
        .order_by(func.count(Search.city).desc())
    )
    total = query.count()
    results = query.offset(offset).limit(limit).all()
    data = [{'city': city, 'count': count} for city, count in results]
    return JSONResponse(
        content={'results': data, 'page': page, 'total': total})


@router.get('/', response_class=HTMLResponse)
async def index(
    request: Request,
    city: str = None,
    db: Session = Depends(get_db)
):
    """
    Главная страница: отображение прогноза погоды и истории поиска.

    Если передан параметр `city`, осуществляется
    перевод и запрос к погодному API.
    """
    history_cookie = request.cookies.get('history')
    history = json.loads(history_cookie) if history_cookie else []
    translated_city = None
    weather = None
    error_message = None
    if city:
        try:
            existing = db.query(Search).filter_by(
                city=city).order_by(Search.timestamp.desc()).first()
            if existing and existing.city_en:
                city_en = existing.city_en
            else:
                city_en = translate(city, 'ru', 'en')
                search_entry = Search(
                    user_id=None,
                    city=city,
                    city_en=city_en,
                    timestamp=datetime.now()
                )
                db.add(search_entry)
                db.commit()
            weather = fetch_weather(city_en)
            if not weather:
                error_message = f"Город '{city}' не найден."
            else:
                translated_city = translate(weather['city'], 'en', 'ru')
                city_stats[weather['city']] = city_stats.get(
                    weather['city'], 0) + 1
        except Exception:
            error_message = 'Ошибка при получении данных с сервера погоды.'
    context = {
        'request': request,
        'weather': weather,
        'translated_city': translated_city,
        'history': history,
    }
    if error_message:
        context['error'] = error_message
    return templates.TemplateResponse('index.html', context)


@router.post('/', response_class=HTMLResponse)
async def get_weather(
    request: Request,
    response: Response,
    city: str = Form(..., description='Название города'),
    db: Session = Depends(get_db)
):
    """
    Обрабатывает форму поиска города, сохраняет
    историю и перенаправляет на главную страницу с прогнозом.
    """
    history_cookie = request.cookies.get('history')
    history = json.loads(history_cookie) if history_cookie else []
    if city not in history:
        history.append(city)
        history = history[-10:]

    city_en = translate(city, 'ru', 'en')
    search_entry = Search(
        user_id=None,
        city=city,
        city_en=city_en,
        timestamp=datetime.now()
    )
    db.add(search_entry)
    db.commit()
    redirect_url = f'/?city={quote(city)}'
    redirect_response = RedirectResponse(
        url=redirect_url,
        status_code=status.HTTP_303_SEE_OTHER
    )
    redirect_response.set_cookie(
        key='history',
        value=json.dumps(history),
        httponly=True
    )
    return redirect_response
