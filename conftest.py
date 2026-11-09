import pytest
from helpers.helpers import generate_random_user_data, register_user, delete_registered_user


@pytest.fixture
def unique_user_payload():
    return generate_random_user_data()


@pytest.fixture
def cleanup_user():
    user_data = {}
    yield user_data
    token = user_data.get("accessToken")
    if token:
        delete_registered_user(token)

@pytest.fixture
def registered_user(unique_user_payload, cleanup_user):

    response = register_user(unique_user_payload)
    data = response.json()
    token = data.get("accessToken")
    cleanup_user["accessToken"] = token
    unique_user_payload["accessToken"] = token

    return unique_user_payload

