import pytest
import allure
from helpers.constants import Urls, Messages
from helpers.helpers import api_client


@allure.epic("Stellar Burgers API")
class TestLoginUser:

    @allure.feature("Авторизация пользователя")
    @allure.story("Логин")
    @allure.title("Успешный логин существующего пользователя")
    def test_login_existing_user_success(self, registered_user):
        payload = {"email": registered_user["email"],
                   "password": registered_user["password"]}
        with allure.step('Логиним пользователя'):
            response = api_client.post(Urls.LOGIN, json=payload)

        with allure.step('Проверить, что код ответа 200'):
            assert response.status_code == 200
        with allure.step('Проверить, что поле success == True'):
            assert response.json()["success"] is True
        with allure.step('Запрос вернул accessToken'):
            assert "accessToken" in response.json()

    @allure.feature("Авторизация пользователя")
    @allure.story("Логин")
    @allure.title("Граничные кейсы: Неверные креденшелы при логине")
    @pytest.mark.parametrize(
        "field, invalid_value",
        [
            ("email", "wrong_@email@ya.ru"),
            ("password", "wrong_password"),
            ("email", ""),
        ],
        ids=["wrong_email", "wrong_password", "empty_email"]
        )
    def test_login_invalid_credentials_unauthorized(self, registered_user, field, invalid_value):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        payload[field] = invalid_value

        with allure.step('Логиним пользователя с неверными креденшелами'):
            response = api_client.post(Urls.LOGIN, json=payload)
        with allure.step('Проверить, что код ответа 401'):
            assert response.status_code == 401
        with allure.step('Проверить, что поле success == False'):
            assert response.json()["success"] is False
        with allure.step(f'Проверить, что поле в поле message содержится текст {Messages.INCORRECT_CREDS_MESSAGE}'):
            assert response.json()["message"] == Messages.INCORRECT_CREDS_MESSAGE
