import pytest
from fastapi.testclient import TestClient
from fastapi_testing import create_test_server
from backend.src.main import app

client = TestClient(app)


def test_get_all_tags():
    response = client.get('api/tags')
    assert response.status_code == 200, 'Не то'
    print(response.json())
    
def test_get_tag_by_id():
    response = client.get('api/tags/{tag_id}')
    assert response.status_code == 200
