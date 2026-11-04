import pytest
import allure
from helpers.constants import Config
from helpers.helpers import generate_random_user_data, api_client, delete_registered_user


@allure.epic("Stellar Burgers API")
class TestCreateOrder:

    @allure.feature("Управление заказами")
    @allure.story("Создание заказа")
    @allure.title("Создание заказа: Валидные ингредиенты, без ингредиентов, невалидный хеш")
    @pytest.mark.parametrize("has_ingredients, valid_hash", [
        (True, True),     # с валидными ингредиентами
        (False, True),    # без ингредиентов
        (True, False),    # с неверным хешем ингредиента
    ], ids=["valid_ingredients", "empty_ingredients", "invalid_hash"])
    def test_create_order_return_valid_response(self, registered_user, has_ingredients, valid_hash):
        headers = {
            "Authorization": registered_user["accessToken"]}

        if not has_ingredients:
            payload = {"ingredients": []}
        elif not valid_hash:
            payload = {"ingredients": [Config.INVALID_INGREDIENT_HASH]}
        else:
            payload = {"ingredients": Config.VALID_INGREDIENT_HASHES}

        response = api_client.post(Config.ORDERS,
                                   headers=headers, json=payload)

        if not has_ingredients:
            assert response.status_code == 400
            assert response.json()["success"] is False
            assert response.json()[
                "message"] == "Ingredient ids must be provided"
        elif not valid_hash:
            assert response.status_code == 500
        else:
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "order" in response.json()
