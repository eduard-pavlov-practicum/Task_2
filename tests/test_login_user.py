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
        response = api_client.post(Config.LOGIN, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True
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

        response = api_client.post(Config.LOGIN, json=payload)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "email or password are incorrect"
