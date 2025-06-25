import time


class Url:
    BASE_URL = 'https://stellarburgers.nomoreparties.site'
    REGISTER = '/api/auth/register'
    DELETE_USER = '/api/auth/user'
    AUTH_USER = '/api/auth/login'
    UPDATE_USER = '/api/auth/user'
    ORDERS = '/api/orders'
    INGREDIENTS = '/api/ingredients'

class UserCreationData:
    PAYLOAD = {
        "email": f"user_{time.time()}@example.com",
        "password": "ValidP@ssw0rd",
        "name": "Test User"
    }
    PAYLOAD_EMPTY = {}

class Messages:
    EXPECTED_MESSAGE = 'Email, password and name are required fields'
    EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH = 'email or password are incorrect'
    MESSAGE_UPDATE_WITHOUT_AUTH = 'You should be authorised'
    MESSAGE_UPDATE_EXISTING_EMAIL = 'User with such email already exists'
    MESSAGE_GET_ORDERS_UNAUTHORIZED = 'You should be authorised'
    MESSAGE_CREATE_ORDER_NO_INGREDIENTS = 'Ingredient ids must be provided'

class Ingredients:
    MOCK_INGREDIENTS = [{
                    "_id": "61c0c5a71d1f82001bdaaa6d",
                    "name": "Флюоресцентная булка R2-D3",
                    "type": "bun",
                    "proteins": 44,
                    "fat": 26,
                    "carbohydrates": 85,
                    "calories": 643,
                    "price": 988,
                    "image": "https://code.s3.yandex.net/react/code/bun-01.png",
                    "image_mobile": "https://code.s3.yandex.net/react/code/bun-01-mobile.png",
                    "image_large": "https://code.s3.yandex.net/react/code/bun-01-large.png",
                    "__v": 0
                },
                {
                    "_id": "61c0c5a71d1f82001bdaaa6f",
                    "name": "Мясо бессмертных моллюсков Protostomia",
                    "type": "main",
                    "proteins": 433,
                    "fat": 244,
                    "carbohydrates": 33,
                    "calories": 420,
                    "price": 1337,
                    "image": "https://code.s3.yandex.net/react/code/meat-02.png",
                    "image_mobile": "https://code.s3.yandex.net/react/code/meat-02-mobile.png",
                    "image_large": "https://code.s3.yandex.net/react/code/meat-02-large.png",
                    "__v": 0
                }]

    VALID_INGREDIENTS = [
        '61c0c5a71d1f82001bdaaa6d',  # Флюоресцентная булка R2-D3
        '61c0c5a71d1f82001bdaaa6f'  # Мясо бессмертных моллюсков Protostomia
    ]