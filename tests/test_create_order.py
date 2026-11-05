import pytest
import allure
from helpers.constants import Config
from helpers.helpers import api_client


@allure.epic("Stellar Burgers API")
class TestCreateOrder:

    @allure.feature("Управление заказами")
    @allure.story("Создание заказа")
    @allure.title("Создание заказа авторизованным пользователем: Валидные ингредиенты, без ингредиентов, невалидный хеш")
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
        with allure.step('Создаем заказ'):
            response = api_client.post(
                Config.ORDERS, headers=headers, json=payload)

        if not has_ingredients:
            with allure.step('Проверить, что код ответа 200'):
                assert response.status_code == 400
            with allure.step('Проверить, что поле success == False'):
                assert response.json()["success"] is False
            with allure.step(f'Проверить, что поле в поле message содержится текст {Config.INGREDIENT_MUST_PROVIDED_MESSAGE}'):
                assert response.json()[
                    "message"] == Config.INGREDIENT_MUST_PROVIDED_MESSAGE
        elif not valid_hash:
            with allure.step('Проверить, что код ответа 500'):
                assert response.status_code == 500
        else:
            with allure.step('Проверить, что код ответа 200'):
                assert response.status_code == 200
            with allure.step('Проверить, что поле success == True'):
                assert response.json()["success"] is True
            with allure.step('Проверить, что в ответе есть order'):
                assert "order" in response.json()

    @allure.feature("Управление заказами")
    @allure.story("Создание заказа")
    @allure.title("Создание заказа не авторизованным пользователем: Валидные ингредиенты")
    def test_create_order_not_authorized_user_redirect_to_login(self):

        payload = {"ingredients": Config.VALID_INGREDIENT_HASHES}
        with allure.step('Создаем заказ'):
            response = api_client.post(Config.ORDERS, json=payload)

        # Проверяем, что произошёл редирект (вся группа 3хх кодов, так как в доке не указан конкретный код)
        with allure.step('Проверить, что код ответа из группы 300'):
            assert response.status_code // 100 == 3, f"Ожидался статус 3xx, получен {response.status_code}"
        # Проверяем, что Location header указывает на правильный URL
        with allure.step(f'Проверить, что заголовок Location содержит url {Config.REDIRECT_LOGIN}'):
            assert response.headers.get("Location") == Config.REDIRECT_LOGIN, \
                f"Ожидалось Location: {Config.REDIRECT_LOGIN}, получено {response.headers.get('Location')}"
