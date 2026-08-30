"""Модуль ждя тестирования контента tag."""


def test_get_tag_list(tag_url, tags, auth_client):
    response = auth_client.get(tag_url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10, f'Ожидалось 10 объектов, получено {len(data)}'
