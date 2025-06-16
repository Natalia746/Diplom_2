import allure
import copy
import pytest
import requests
import time
from data import *
from common_test_methods import *



@allure.epic("API Тесты")
@allure.feature("Регистрация пользователя POST https://stellarburgers.nomoreparties.site/api/auth/register")
class TestUserRegistration:

    @allure.story("Успешная регистрация")
    @allure.title("Проверка успешной регистрации нового пользователя")
    def test_create_unique_user_success(self, registered_user):
        with allure.step("Проверить структуру данных зарегистрированного пользователя"):
            allure.attach(str(registered_user), name="Данные пользователя")
            assert isinstance(registered_user['email'], str)
            assert '@' in registered_user['email']
            assert isinstance(registered_user['name'], str)
            assert isinstance(registered_user['token'], str)
            assert registered_user['token'].startswith('Bearer ')

    @allure.story("Неуспешная регистрация")
    @allure.title("Попытка регистрации уже существующего пользователя")
    def test_create_existing_user_fail(self, registered_user):
        with allure.step("Подготовить данные существующего пользователя"):
            payload = {
                "email": registered_user['email'],
                "password": registered_user['password'],
                "name": registered_user['name']
            }
            allure.attach(str(payload), name="Тестовые данные")

        with allure.step("Отправить запрос на регистрацию"):
            test_data = payload
            response = send_register_request(test_data)
            allure.attach(str(response.status_code), name="Код ответа")
            allure.attach(response.text, name="Тело ответа")

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data['success'] is False
            assert response_data['message'] == 'User already exists'

    @allure.story("Валидация полей")
    @allure.title("Проверка валидации обязательных полей при регистрации")
    @pytest.mark.parametrize('field, action, expected_msg', [
        ('email', 'delete', Messages.EXPECTED_MESSAGE),
        ('password', 'delete', Messages.EXPECTED_MESSAGE),
        ('name', 'delete', Messages.EXPECTED_MESSAGE),
        ('email', 'empty', Messages.EXPECTED_MESSAGE),
        ('password', 'empty', Messages.EXPECTED_MESSAGE),
        ('name', 'empty', Messages.EXPECTED_MESSAGE),
    ])
    def test_user_creation_field_validation(self, field, action, expected_msg):
        with allure.step(f"Подготовить тестовые данные (поле {field}, действие: {action})"):
            test_data = copy.deepcopy(UserCreationData.PAYLOAD)
            if action == 'delete':
                del test_data[field]
            elif action == 'empty':
                test_data[field] = ""
            allure.attach(str(test_data), name="Модифицированные данные")

        with allure.step("Отправить запрос на регистрацию"):
            response = requests.post(
                Url.BASE_URL + Url.REGISTER,
                json=test_data
            )
            allure.attach(str(response.status_code), name="Код ответа")
            allure.attach(response.text, name="Тело ответа")

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data['success'] is False
            assert response_data['message'] == expected_msg

    @allure.story("Валидация полей")
    @allure.title("Проверка регистрации с пустым JSON")
    def test_user_creation_empty_json(self):
        with allure.step("Подготовить пустой JSON"):
            test_data = UserCreationData.PAYLOAD_EMPTY
            allure.attach(str(test_data), name="Тестовые данные (пустой JSON)")

            response = send_register_request(test_data)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data['success'] is False
            assert response_data['message'] == Messages.EXPECTED_MESSAGE

