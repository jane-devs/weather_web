import requests
from datetime import datetime


def weathercode_to_icon(code: int):
    """
    Возвращает описание и иконку по коду погодного состояния.
    """
    mapping = {
        0: ('Ясно', '☀️'),
        1: ('Частично облачно', '🌤️'),
        2: ('Облачно', '☁️'),
        3: ('Пасмурно', '☁️'),
        45: ('Туман', '🌫️'),
        48: ('Иней', '🌫️'),
        51: ('Лёгкий дождь', '🌦️'),
        53: ('Умеренный дождь', '🌧️'),
        55: ('Сильный дождь', '🌧️'),
        61: ('Дождь', '🌧️'),
        63: ('Сильный дождь', '🌧️'),
        65: ('Очень сильный дождь', '🌧️'),
        71: ('Снег', '❄️'),
        73: ('Снег', '❄️'),
        75: ('Сильный снег', '❄️'),
        80: ('Ливни', '🌧️'),
        81: ('Сильные ливни', '🌧️'),
        82: ('Очень сильные ливни', '🌧️'),
        95: ('Гроза', '⛈️'),
        96: ('Гроза с легким градом', '⛈️'),
        99: ('Гроза с градом', '⛈️'),
    }
    return mapping.get(code, ('Неизвестно', '❓'))


def fetch_weather(city_en: str):
    """
    Получает прогноз погоды на текущий день и завтра
    по переведённому названию города.
    """
    location = search_city(city_en)
    lat, lon, name = (
        location[0]['latitude'],
        location[0]['longitude'],
        location[0]['name']
    )

    url = (
        f'https://api.open-meteo.com/v1/forecast?'
        f'latitude={lat}&longitude={lon}&current_weather=true&'
        f'hourly=relative_humidity_2m,pressure_msl,precipitation&'
        f'daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum,windspeed_10m_max&' # noqa
        f'timezone=Europe/Moscow'
    )

    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()

    current = data.get('current_weather')
    daily = data.get('daily', {})

    if not current or not daily:
        return None

    dt_str = current.get('time')
    dt_obj = datetime.fromisoformat(dt_str) if dt_str else None
    dt_formatted = dt_obj.strftime('%d.%m.%Y %H:%M') if dt_obj else dt_str
    condition_text, condition_icon = weathercode_to_icon(
        current.get('weathercode'))

    def parse_day(index):
        weathercode = daily['weathercode'][index]
        cond_text, cond_icon = weathercode_to_icon(weathercode)
        return {
            'date': daily['time'][index],
            'temp_max': daily['temperature_2m_max'][index],
            'temp_min': daily['temperature_2m_min'][index],
            'condition_text': cond_text,
            'condition_icon': cond_icon,
            'precipitation': daily['precipitation_sum'][index],
        }

    weather_info = {
        'city': name,
        'temp': current.get('temperature'),
        'condition_text': condition_text,
        'condition_icon': condition_icon,
        'datetime': dt_formatted,
        'today': parse_day(0) if len(daily.get('time', [])) > 0 else None,
        'tomorrow': parse_day(1) if len(daily.get('time', [])) > 1 else None,
    }

    return weather_info


def search_city(city_en: str):
    """
    Выполняет поиск города по его названию на английском языке
    с помощью Open-Meteo Geocoding API.
    """
    city_en = city_en.replace(' - ', ' ').replace('-', ' ').strip()
    url = f'https://geocoding-api.open-meteo.com/v1/search?name={city_en}&count=5' # noqa
    res = requests.get(url)
    results = res.json().get('results', [])
    if not results:
        raise ValueError(f"Город '{city_en}' не найден.")
    return results
