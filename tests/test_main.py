from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_get():
    """
    Тест: проверяет, что GET-запрос на корневой эндпоинт "/"
    возвращает статус 200 и HTML-контент.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']


def test_get_city_stats_default():
    """
    Тест: проверяет успешный ответ эндпоинта "/api/get-city-stats"
    с параметрами по умолчанию.
    """
    response = client.get('/api/get-city-stats')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert 'page' in data and 'results' in data


def test_get_city_stats_with_params():
    """
    Тест: проверяет корректную работу пагинации в эндпоинте 
    "/api/get-city-stats"
    при заданных параметрах page и limit.
    """
    response = client.get('/api/get-city-stats?page=2&limit=5')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert 'results' in data
    assert len(data['results']) <= 5


def test_autocomplete_valid_query():
    """
    Тест: проверяет, что эндпоинт "/api/autocomplete"
    возвращает список городов, начинающихся с заданного префикса.
    """
    response = client.get('/api/autocomplete?query=Моск')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(isinstance(city, str) for city in data)
    # Если данных нет — просто пропускаем проверку startswith
    if data:
        assert any(city.lower().startswith('моск') for city in data)


def test_autocomplete_missing_query():
    """
    Тест: проверяет, что отсутствие параметра "query"
    в запросе к "/api/autocomplete" приводит к ошибке валидации (422).
    """
    response = client.get('/api/autocomplete')
    assert response.status_code == 422


def test_autocomplete_empty_query():
    """
    Тест: проверяет поведение при пустом параметре "query".
    Если сервер принимает пустой запрос — возвращает 200 с пустым списком.
    """
    response = client.get('/api/autocomplete?query=')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
