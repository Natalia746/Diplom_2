import pytest
import requests
import time
from data import *
from unittest.mock import MagicMock



@pytest.fixture
def registered_user():
    email = f'test_user_{time.time()}@example.com'
    password = 'P@ssw0rd123'
    name = 'Test User'

    user_data = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(
        Url.BASE_URL + Url.REGISTER,
        json=user_data
    )
    assert response.status_code == 200, f"Failed to register user: {response.text}"

    token = response.json()['accessToken']
    user_data['token'] = token

    yield user_data

    # Удаление пользователя после теста
    delete_response = requests.delete(
        Url.BASE_URL + Url.DELETE_USER,
        headers={'Authorization': token}
    )
    assert delete_response.status_code == 202, f"Failed to delete user: {delete_response.text}"


@pytest.fixture
def unauthorized_mock():
    mock = MagicMock()
    mock.status_code = 401
    mock.json.return_value = {
        "success": False,
        "message": Messages.MESSAGE_UPDATE_WITHOUT_AUTH
    }
    return mock





