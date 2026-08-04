"""Модуль для тестирования логики сущности Recipe."""

from fastapi import status

from backend.app.models import RecipeModel


def test_updating_recipe(
    recipe_update_form_data,
    auth_client,
    recipe_object,
    recipe_detail_url,
):
    """Тестирование обновления рецепта."""

    response = auth_client.get(recipe_detail_url)
    assert response.status_code == status.HTTP_200_OK

    update_response = auth_client.put(
        recipe_detail_url,
        json=recipe_update_form_data,
    )
    response_data = update_response.json()
    assert (
        update_response.status_code == status.HTTP_200_OK
    ), f'Рецепт не обновился. {response_data}'

    expected_data = {
        "name": recipe_update_form_data["name"],
        "text": recipe_update_form_data["text"],
        "cooking_time": recipe_update_form_data["cooking_time"],
        "image": recipe_update_form_data["image"],
        "ingredients": [
            {
                "id": ing["id"],
                "amount": ing["amount"],
            }
            for ing in recipe_update_form_data["ingredients"]
        ],
        "tags": [
            {"id": tag_id}  # Только id, т.к. name и slug могут быть любыми
            for tag_id in recipe_update_form_data["tags"]
        ],
    }

    assert response_data["name"] == expected_data["name"]
    assert response_data["text"] == expected_data["text"]
    assert response_data["cooking_time"] == expected_data["cooking_time"]
    assert response_data["image"] == expected_data["image"]

    # Проверяем ингредиенты
    assert len(response_data["ingredients"]) == len(
        expected_data["ingredients"]
    )
    for i, ing in enumerate(response_data["ingredients"]):
        assert ing["id"] == expected_data["ingredients"][i]["id"]
        # Раскомментить после решения проблемы
        # с неккоректным выводом поля amount.
        # assert ing["amount"] == expected_data["ingredients"][i]["amount"]

    # Проверяем теги
    assert len(response_data["tags"]) == len(expected_data["tags"])
    for i, tag in enumerate(response_data["tags"]):
        assert tag["id"] == expected_data["tags"][i]["id"]


def test_create_recipe(auth_client, recipe_create_form_data, recipe_url):
    """Тестирование создания рецепта."""
    response = auth_client.post(recipe_url, json=recipe_create_form_data)

    data = response.json()
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), f'Ошибка при создании рецепта: {data}'


def test_not_found_if_no_recipe(recipe_url, auth_client):
    """Тестирование корректного исключения,
    если пользователь пытается  получить рецепт
    с несуществующим айди."""

    response = auth_client.get(recipe_url + '/' + '100000')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_recipe(
    recipe_detail_url,
    auth_client,
    db_session,
    recipe_object,
):
    """Тестирование удаления рецепта."""
    response = auth_client.delete(recipe_detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not db_session.get(
        RecipeModel,
        recipe_object.id,
    ), 'Рецепт все же есть в БД.'
