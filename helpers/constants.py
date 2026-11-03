from dataclasses import dataclass


@dataclass
class Config:
    BASE_URL = "https://stellarburgers.education-services.ru"

    REGISTER = f"{BASE_URL}/api/auth/register"
    LOGIN = f"{BASE_URL}/api/auth/login"
    USER = f"{BASE_URL}/api/auth/user"
    ORDERS = f"{BASE_URL}/api/orders"

    VALID_INGREDIENT_HASHES = [
        "6ae327a87e8698001b542b3b", "6ae327a87e8698001b542b40"]
    INVALID_INGREDIENT_HASH = VALID_INGREDIENT_HASHES[0][::-1]
