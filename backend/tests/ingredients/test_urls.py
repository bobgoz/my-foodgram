def test_ingredient_url(
    ingredient_url,
    client,
):
    response = client.get(ingredient_url)
    assert response.status_code == 200, f'{response.json()}'


def test_get_ingredient_by_id(
    ingredient_detail_url, ingredient_object, client
):
    response = client.get(ingredient_detail_url)
    assert response.status_code == 200, f'{response.json()}'
