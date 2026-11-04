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

        # Создадим сначала 1 заказ для этого пользователя, чтобы в списке что-то было
        api_client.post(Config.ORDERS, headers=headers, json={
            "ingredients": Config.VALID_INGREDIENT_HASHES})

        # Делаем запрос на получение
        response = api_client.get(Config.ORDERS, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert isinstance(response.json()["orders"], list)
        assert len(response.json()["orders"]) > 0

    @allure.feature("Управление заказами")
    @allure.story("Получение заказов пользователя")
    @allure.title("Неавторизованный пользователь: Ошибка при попытке получения списка")
    def test_get_user_orders_unauthorized_forbidden(self):
        response = api_client.get(Config.ORDERS)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "You should be authorised"
