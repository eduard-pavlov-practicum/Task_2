import pytest
import allure
from helpers.constants import Config
from helpers.helpers import api_client, delete_registered_user


@allure.epic("Stellar Burgers API")
class TestRegisterUser:

    @allure.feature("Создание пользователя")
    @allure.story("Регистрация")
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, unique_user_payload):
        with allure.step('Регистрируем нового пользователя'):
            response = api_client.post(
                Config.REGISTER, json=unique_user_payload)
        with allure.step('Проверить, что код ответа 200'):
            assert response.status_code == 200
        with allure.step('Проверить, что поле success == True'):
            assert response.json()["success"] is True

        # Подчищаем за собой, так как фикстура не используется
        token = response.json().get("accessToken")
        if token:
            delete_registered_user(token)

    @allure.feature("Создание пользователя")
    @allure.story("Регистрация")
    @allure.title("Ошибка при создании уже зарегистрированного пользователя")
    def test_create_duplicate_user_forbidden(self, registered_user):
        # Пытаемся повторно зарегистрировать данные из фикстуры registered_user
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        }
        with allure.step('Регистрируем того же самого пользователя'):
            response = api_client.post(Config.REGISTER, json=payload)
        with allure.step('Проверить, что код ответа 403'):
            assert response.status_code == 403
        with allure.step('Проверить, что поле success == False'):
            assert response.json()["success"] is False
        with allure.step(f'Проверить, что поле в поле message содержится текст {Config.USER_EXISTS_MESSAGE}'):
            assert response.json()["message"] == Config.USER_EXISTS_MESSAGE

    @allure.feature("Создание пользователя")
    @allure.story("Регистрация")
    @allure.title("Граничные кейсы: Пропуск обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, unique_user_payload, missing_field):
        del unique_user_payload[missing_field]
        with allure.step(f'Регистрируем пользователя без указания {missing_field}'):
            response = api_client.post(
                Config.REGISTER, json=unique_user_payload)
        with allure.step('Проверить, что код ответа 403'):
            assert response.status_code == 403
        with allure.step('Проверить, что поле success == False'):
            assert response.json()["success"] is False
        with allure.step(f'Проверить, что поле в поле message содержится текст {Config.REQUIRED_FIELDS}'):
            assert response.json()["message"] == Config.REQUIRED_FIELDS
