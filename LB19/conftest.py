import pytest
from fastapi.testclient import TestClient
from main_views import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)