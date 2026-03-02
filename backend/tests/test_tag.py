import pytest
from fastapi.testclient import TestClient
from fastapi_testing import create_test_server
from backend.src.main import app

client = TestClient(app)


def test_get_all_tags():
    response = client.get('api/tags')
    assert response.status_code == 404, 'Не то'
    assert response.json() == {'da': '2'}
