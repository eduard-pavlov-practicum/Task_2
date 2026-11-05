import pytest
import allure
from helpers.constants import Config
from helpers.helpers import api_client


@allure.epic("Stellar Burgers API")
class TestUserOrders:

    @allure.feature("Управление заказами")
    @allure.story("Получение заказов пользователя")
    @allure.title("Авторизованный пользователь: Успешное получение списка своих заказов")
    def test_get_user_orders_authorized_success(self, registered_user):
        headers = {"Authorization": registered_user["accessToken"]}

        with allure.step('Создадим сначала 1 заказ для этого пользователя, чтобы в списке что-то было'):
            api_client.post(Config.ORDERS, headers=headers, json={
                            "ingredients": Config.VALID_INGREDIENT_HASHES})

        with allure.step('Получаем список заказов пользователя'):
            response = api_client.get(Config.ORDERS, headers=headers)
        with allure.step('Проверить, что код ответа 200'):
            assert response.status_code == 200
        with allure.step('Проверить, что поле success == True'):
            assert response.json()["success"] is True
        with allure.step('Проверить, что в ответе есть список orders'):
            assert isinstance(response.json()["orders"], list)
        with allure.step('Проверить, что список orders не пуст'):
            assert len(response.json()["orders"]) > 0

    @allure.feature("Управление заказами")
    @allure.story("Получение заказов пользователя")
    @allure.title("Неавторизованный пользователь: Ошибка при попытке получения списка")
    def test_get_user_orders_unauthorized_forbidden(self):
        with allure.step('Получаем список заказов'):
            response = api_client.get(Config.ORDERS)

        with allure.step('Проверить, что код ответа 401'):
            assert response.status_code == 401
        with allure.step('Проверить, что поле success == False'):
            assert response.json()["success"] is False
        with allure.step(f'Проверить, что поле в поле message содержится текст {Config.SHOULD_AUTHORIZED_MESSAGE}'):
            assert response.json()[
                "message"] == Config.SHOULD_AUTHORIZED_MESSAGE
