import json
import requests
import allure
from faker import Faker
from helpers.constants import Urls

fake = Faker('ru_RU')


def generate_random_user_data():
    """
    Генератор уникальных и реалистичных данных пользователя с помощью Faker.
    """
    return {
        "email": fake.free_email(),
        "password": fake.password(length=10, special_chars=False),
        "name": fake.first_name()
    }


@allure.step('Создаем нового пользователя')
def register_user(user_data):
    return api_client.post(Urls.REGISTER, json=user_data)


@allure.step('Удаляем созданного пользователя')
def delete_registered_user(token: str):
    headers = {"Authorization": token}
    api_client.delete(Urls.USER, headers=headers)


class ApiClient(requests.Session):
    """
    HTTP-клиент перехватывает все запросы и автоматически логирует их в Allure.
    """

    def request(self, method, url, **kwargs):
        with allure.step(f"API Запрос: {method.upper()} {url}"):
            if "headers" in kwargs:
                allure.attach(json.dumps(
                    kwargs["headers"], indent=2), name="Request Headers", attachment_type=allure.attachment_type.JSON)
            if "json" in kwargs:
                allure.attach(json.dumps(
                    kwargs["json"], indent=2), name="Request Body", attachment_type=allure.attachment_type.JSON)

            response = super().request(method, url, **kwargs)

            allure.attach(str(response.status_code), name="Response Status Code",
                          attachment_type=allure.attachment_type.TEXT)
            try:
                allure.attach(json.dumps(response.json(), indent=2, ensure_ascii=False),
                              name="Response Body", attachment_type=allure.attachment_type.JSON)
            except ValueError:
                allure.attach(response.text, name="Response Text (Not JSON)",
                              attachment_type=allure.attachment_type.TEXT)

            return response


api_client = ApiClient()
