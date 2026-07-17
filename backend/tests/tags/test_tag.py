import pytest


def test_tag_url(
    tag_url,
    client,
):
    response = client.get(tag_url)
    assert response.status_code == 200, f'{response.json()}'


def test_get_tag_by_id(tag_detail_url, tag_object, client):
    response = client.get(tag_detail_url)
    assert response.status_code == 200, f'{response.json()}'


def test_get_tag_list(tag_url, tags, client):
    response = client.get(tag_url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10, f'Ожидалось 10 объектов, получено {len(data)}'
