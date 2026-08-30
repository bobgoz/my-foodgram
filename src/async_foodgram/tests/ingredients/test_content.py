def test_get_ingredient_list(ingredient_url, ingredients, client):
    response = client.get(ingredient_url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10, f'Ожидалось 10 объектов, получено {len(data)}'
