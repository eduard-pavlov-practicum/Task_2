import pytest
import allure
from helpers.constants import Urls, Messages
from helpers.helpers import generate_random_user_data, api_client, register_user, delete_registered_user


@allure.epic("Stellar Burgers API")
class TestChangeUser:
    user_data = generate_random_user_data()

    @allure.feature("Данные пользователя")
    @allure.story("Изменение данных")
    @allure.title("Авторизованный пользователь: Изменение любого поля")
    @pytest.mark.parametrize("field_to_update", [
        ("email"),
        ("name")
    ])
    def test_update_authorized_user_fields_success(self, registered_user, field_to_update):
        headers = {"Authorization": registered_user["accessToken"]}
        new_value = f"updated{registered_user[field_to_update]}"
        payload = {field_to_update: new_value}

        response = api_client.patch(Urls.USER,
                                    headers=headers, json=payload)
        with allure.step('Проверить, что код ответа 200'):
            assert response.status_code == 200
        with allure.step('Проверить, что поле success == True'):
            assert response.json()["success"] is True
        with allure.step(f'Проверить, что у пользователя поле {field_to_update} == {new_value}'):
            assert response.json()["user"][field_to_update] == new_value

    @allure.feature("Данные пользователя")
    @allure.story("Изменение данных")
    @allure.title("Авторизованный пользователь: Новый email от существующего пользователя")
    def test_update_authorized_user_email_by_email_another_user_return_forbidden(self, registered_user):

        test_user_response = register_user(generate_random_user_data())
        test_user_token = test_user_response.json().get("accessToken")

        headers = {"Authorization": test_user_token}
        payload = {'email': registered_user['email']}

        response = api_client.patch(Urls.USER,
                                    headers=headers, json=payload)
        with allure.step('Проверить, что код ответа 403'):
            assert response.status_code == 403

        with allure.step('Проверить, что поле success == False'):
            assert response.json()["success"] is False
        with allure.step(f'Проверить, что поле в поле message содержится текст {Messages.EXISTING_EMAIL_MESSAGE}'):
            assert response.json()["message"] == Messages.EXISTING_EMAIL_MESSAGE
        if test_user_token:
            delete_registered_user(test_user_token)

    @allure.feature("Данные пользователя")
    @allure.story("Изменение данных")
    @allure.title("Неавторизованный пользователь: Попытка изменения полей")
    @pytest.mark.parametrize("field_to_update, new_value", [
        ("email", "not_auth_user@not_auth_user.ru"),
        ("name", "Not Auth User")
    ])
    def test_update_unauthorized_user_fields_forbidden(self, field_to_update, new_value):
        payload = {field_to_update: new_value}
        with allure.step(f'Обновляем поле {field_to_update}'):
            response = api_client.patch(Urls.USER, json=payload)
        with allure.step('Проверить, что код ответа 401'):
            assert response.status_code == 401
        with allure.step('Проверить, что поле success == False'):
            assert response.json()["success"] is False
        with allure.step(f'Проверить, что поле в поле message содержится текст {Messages.SHOULD_AUTHORIZED_MESSAGE}'):
            assert response.json()[
                "message"] == Messages.SHOULD_AUTHORIZED_MESSAGE
