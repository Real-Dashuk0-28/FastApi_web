import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main_views import app

client = TestClient(app)


# =======================================================
# ТЕСТ 1: Проверка корня без параметров
# =======================================================

def test_root_view():
    """Тест эндпоинта '/' без передачи query-параметра 'name'"""

    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["docs"] == "https://example.com/docs"

    assert data["message"] == "Hello, world!"

# =======================================================
# ТЕСТ 2: Проверка корня с разными параметрами (параметризация)
# =======================================================

@pytest.mark.parametrize("name", [
    "Alice",
    "Bob",
    "Charlie",
    "Maria",
    "123",
    "Анна",
    ""
])
def test_root_view_custom_name(name):
    """Параметризованный тест эндпоинта '/' с передачей query-параметра 'name'.
    Кол-во тест == кол-во д в списке выше"""

    # Формируем query-параметры
    # Если name == "", передаём "" словарь (знач по умол)
    if name:
        query_params = {"name": name}
    else:
        query_params = {}

    response = client.get("/", params=query_params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "docs" in data
    assert data["docs"] == "https://example.com/docs"

    if name:
        expected_message = f"Hello, {name}!"
    else:
        expected_message = "Hello, world!"

    assert data["message"] == expected_message