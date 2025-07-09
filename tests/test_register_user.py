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
    @allure.title("Регистрация без обязательного поля")
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_missing_field_validation(self, field):
        test_data = copy.deepcopy(UserCreationData.PAYLOAD)
        del test_data[field]

        with allure.step(f"Отправить запрос без поля {field}"):
            response = requests.post(Url.BASE_URL + Url.REGISTER, json=test_data)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data['success'] is False
            assert response_data['message'] == Messages.EXPECTED_MESSAGE

    @allure.title("Регистрация с пустым обязательным полем")
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_empty_field_validation(self, field):
        test_data = copy.deepcopy(UserCreationData.PAYLOAD)
        test_data[field] = ""

        with allure.step(f"Отправить запрос с пустым полем {field}"):
            response = requests.post(Url.BASE_URL + Url.REGISTER, json=test_data)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data['success'] is False
            assert response_data['message'] == Messages.EXPECTED_MESSAGE

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

