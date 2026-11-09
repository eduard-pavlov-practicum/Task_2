import pytest
import allure
from helpers.constants import Urls, Ingredients, Messages
from helpers.helpers import api_client


@allure.epic("Stellar Burgers API")
class TestCreateOrder:

    @allure.feature("Управление заказами")
    @allure.story("Создание заказа")
    @allure.title("Создание заказа авторизованным пользователем: Валидные ингредиенты")
    def test_create_order_with_valid_request_return_successful_response(self, registered_user):
        headers = {
            "Authorization": registered_user["accessToken"]}

        payload = {"ingredients": Ingredients.VALID_INGREDIENT_HASHES}

        with allure.step('Создаем заказ'):
            response = api_client.post(
                Urls.ORDERS, headers=headers, json=payload)

        with allure.step('Проверить, что код ответа 200'):
            assert response.status_code == 200
        with allure.step('Проверить, что поле success == True'):
            assert response.json()["success"] is True
        with allure.step('Проверить, что в ответе есть order'):
            assert "order" in response.json()


    @allure.feature("Управление заказами")
    @allure.story("Создание заказа")
    @allure.title("Создание заказа авторизованным пользователем: Без ингредиентов")
    def test_create_order_without_ingredients_return_400_with_message(self, registered_user):
        headers = {
            "Authorization": registered_user["accessToken"]}

        payload = {"ingredients": []}
        
        with allure.step('Создаем заказ'):
            response = api_client.post(
                Urls.ORDERS, headers=headers, json=payload)

        with allure.step('Проверить, что код ответа 400'):
            assert response.status_code == 400
        with allure.step('Проверить, что поле success == False'):
            assert response.json()["success"] is False
        with allure.step(f'Проверить, что поле в поле message содержится текст {Messages.INGREDIENT_MUST_PROVIDED_MESSAGE}'):
            assert response.json()[
                "message"] == Messages.INGREDIENT_MUST_PROVIDED_MESSAGE


    @allure.feature("Управление заказами")
    @allure.story("Создание заказа")
    @allure.title("Создание заказа авторизованным пользователем: Невалидный хеш")
    def test_create_order_invalid_ingredients_return_500(self, registered_user):
        headers = {
            "Authorization": registered_user["accessToken"]}

        payload = {"ingredients": [Ingredients.INVALID_INGREDIENT_HASH]}

        with allure.step('Создаем заказ'):
            response = api_client.post(
                Urls.ORDERS, headers=headers, json=payload)

        with allure.step('Проверить, что код ответа 500'):
            assert response.status_code == 500


    @allure.feature("Управление заказами")
    @allure.story("Создание заказа")
    @allure.title("Создание заказа не авторизованным пользователем: Валидные ингредиенты")
    def test_create_order_not_authorized_user_redirect_to_login(self):

        payload = {"ingredients": Ingredients.VALID_INGREDIENT_HASHES}
        with allure.step('Создаем заказ'):
            response = api_client.post(Urls.ORDERS, json=payload)

        # Проверяем, что произошёл редирект (вся группа 3хх кодов, так как в доке не указан конкретный код)
        with allure.step('Проверить, что код ответа из группы 300'):
            assert response.status_code // 100 == 3, f"Ожидался статус 3xx, получен {response.status_code}"
        # Проверяем, что Location header указывает на правильный URL
        with allure.step(f'Проверить, что заголовок Location содержит url {Urls.REDIRECT_LOGIN}'):
            assert response.headers.get("Location") == Urls.REDIRECT_LOGIN, \
                f"Ожидалось Location: {Urls.REDIRECT_LOGIN}, получено {response.headers.get('Location')}"
