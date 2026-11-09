from dataclasses import dataclass


@dataclass
class Urls:
    BASE_URL = "https://stellarburgers.education-services.ru"

    REGISTER = f"{BASE_URL}/api/auth/register"
    LOGIN = f"{BASE_URL}/api/auth/login"
    USER = f"{BASE_URL}/api/auth/user"
    ORDERS = f"{BASE_URL}/api/orders"
    REDIRECT_LOGIN = f"{BASE_URL}/login"


@dataclass
class Ingredients:
    VALID_INGREDIENT_HASHES = [
        "6ae327a87e8698001b542b3b", "6ae327a87e8698001b542b40"]
    INVALID_INGREDIENT_HASH = VALID_INGREDIENT_HASHES[0][::-1]


@dataclass
class Messages:
    EXISTING_EMAIL_MESSAGE = "User with such email already exists"
    SHOULD_AUTHORIZED_MESSAGE = "You should be authorised"
    INGREDIENT_MUST_PROVIDED_MESSAGE = "Ingredient ids must be provided"
    USER_EXISTS_MESSAGE = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INCORRECT_CREDS_MESSAGE = "email or password are incorrect"
