import pytest
from helpers.constants import Config
from helpers.helpers import generate_random_user_data, register_user, delete_registered_user


@pytest.fixture
def unique_user_payload():
    return generate_random_user_data()


@pytest.fixture
def registered_user(unique_user_payload):

    response = register_user(unique_user_payload)
    data = response.json()

    unique_user_payload["accessToken"] = data.get("accessToken")

    yield unique_user_payload

    token = unique_user_payload.get("accessToken")
    if token:
        delete_registered_user(token)
