import pytest
import allure
from helpers.constants import Config
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
            response = api_client.post(Config.LOGIN, json=payload)

        with allure.step('Проверить, что код ответа 200'):
            assert response.status_code == 200
        with allure.step('Проверить, что поле success == True'):
            assert response.json()["success"] is True
        with allure.step('Запрос вернул accessToken'):
            assert "accessToken" in response.json()

    @allure.feature("Авторизация пользователя")
    @allure.story("Логин")
    @allure.title("Граничные кейсы: Неверные креденшелы при логине")
    @pytest.mark.parametrize("payload_modifier", [
        {"email": "wrong_@email@ya.ru", "password": "valid_password"},
        {"email": "valid_email@ya.ru", "password": "wrong_password"},
        {"email": "", "password": "valid_password"}
    ], ids=["wrong_email", "wrong_password", "empty_email"])
    def test_login_invalid_credentials_unauthorized(self, registered_user, payload_modifier):
        payload = {"email": registered_user["email"],
                   "password": registered_user["password"]}
        payload.update(payload_modifier)

        if payload_modifier.get("email") == "valid_email@ya.ru":
            payload["email"] = registered_user["email"]
        if payload_modifier.get("password") == "valid_password":
            payload["password"] = registered_user["password"]
        with allure.step('Логиним пользователя с неверными креденшелами'):
            response = api_client.post(Config.LOGIN, json=payload)
        with allure.step('Проверить, что код ответа 401'):
            assert response.status_code == 401
        with allure.step('Проверить, что поле success == False'):
            assert response.json()["success"] is False
        with allure.step(f'Проверить, что поле в поле message содержится текст {Config.INCORRECT_CREDS_MESSAGE}'):
            assert response.json()["message"] == Config.INCORRECT_CREDS_MESSAGE
