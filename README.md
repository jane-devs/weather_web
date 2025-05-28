<img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white&style=for-the-badge" />
<img src="https://img.shields.io/badge/FastAPI-0.110.0-green?logo=fastapi&logoColor=white&style=for-the-badge" />
<img src="https://img.shields.io/badge/uvicorn-0.29.0-blue?logo=python&style=for-the-badge" />
<img src="https://img.shields.io/badge/Pytest-8.1.1-yellow?style=for-the-badge" />
<img src="https://img.shields.io/badge/Docker-Supported-informational?logo=docker&style=for-the-badge" />

# Weather Forecast Platform

Проект реализован в рамках тестового задания для o-complex. Приложение позволяет пользователю получить актуальный прогноз погоды для выбранного города с возможностью автодополнения, сохранением истории запросов и статистикой по частоте введённых городов.

Реализовано:
- [x] веб-фронт
- [x] api-запросы
- [x] тесты
- [x] контейнеризация
- [x] автодополнения (подсказки)
- [x] список просмотренных ранее городов с возможностью одним кликом снова посмотреть там погоду
- [x] сохраняется история в БД
- [x] есть api для просмотра статистики

Можно улучшить:
- [ ] валидация данных
- [ ] больше тестирования
- [ ] заглушки для веб-фронта при ошибках
- [ ] настройка миграций

---

## Оглавление

- [Описание проекта](#описание-проекта)  
- [Функциональность](#функциональность)  
- [Стек](#стек)  
- [Установка](#установка)  
- [Запуск](#запуск)  
- [Тестирование](#тестирование)  
- [API](#api)  
- [Документация API](#документация-api)  
- [Автор](#автор)

---

## Описание проекта

**Weather PLUS Platform** — веб-приложение, предоставляющее прогноз погоды на ближайшие часы/дни по введённому пользователем городу. Используется API open-meteo для получения метеоданных. Пользователю предлагается:

- Удобный ввод с автодополнением
- Повторное предложение последнего города
- Сохранение истории поиска
- API со статистикой запросов

---

## Функциональность

- 🔎 Автодополнение при вводе города  
- 🌤 Получение прогноза погоды на ближайшее время  
- 📁 Сохранение истории поисков  
- 📊 API со статистикой по введённым городам  
- 🐳 Поддержка Docker  
- ✅ Юнит-тесты с использованием `pytest`

---

## Стек

- Python 3.11  
- FastAPI  
- Uvicorn  
- SQLite  
- Requests  
- Pytest  
- Docker
- Jinja2

---

## Установка

```
git clone https://github.com/jane-devs/weather-web.git
cd weather-web
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
```

---

## Запуск

```
uvicorn app.main:app --reload
```
Сайт доступен в браузере: `http://localhost:8000`

---

## Запуск через Docker

```
docker build -t weather-app .

docker run -p 8000:8000 weather-app
```

Сайт доступен в браузере: `http://localhost:8000`

---

## Тестирование

Для запуска тестов из weather_web:

```
python -m pytest tests/test_main.py
```

---

## API

- POST /?city=Астрахань
Получить прогноз погоды по городу.

- GET /api/get-city-stats
Получить статистику запросов по городам.

---

## Документация API

Автодокументация доступна по эндпоинту `/docs`

---

## Автор
Евгения Скуратова
tg:@janedoel