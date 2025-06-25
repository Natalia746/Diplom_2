import allure
import pytest
import requests
from data import *
from common_test_methods import *

@allure.epic("API Тесты")
@allure.feature("Авторизация пользователя POST https://stellarburgers.nomoreparties.site/api/auth/login ")
@allure.story("Вход существующего пользователя")
@allure.title("Успешная авторизация зарегистрированного пользователя")
class TestLoginUser:
    def test_login_with_existing_user(self, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        with allure.step("Подготовить данные для авторизации"):
            allure.attach(str(login_data), name="Данные для входа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Отправить запрос на авторизацию"):
            response = send_auth_request(login_data)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 200, "Ожидается успешная авторизация (код 200)"
            response_data = response.json()

            assert response_data["success"] is True, "Флаг успеха должен быть True"
            assert "accessToken" in response_data, "В ответе должен быть accessToken"
            assert "refreshToken" in response_data, "В ответе должен быть refreshToken"

            with allure.step("Проверить структуру токенов"):
                assert response_data["accessToken"].startswith("Bearer "), "AccessToken должен начинаться с 'Bearer '"
                assert len(response_data["refreshToken"]) > 0, "RefreshToken не должен быть пустым"

    @allure.title("Неуспешная авторизация с неверным паролем")
    @pytest.mark.parametrize("wrong_password", ["wrong_password", "invalid_123", ""])
    def test_wrong_password_login(self, registered_user, wrong_password):
        login_data = {
            "email": registered_user["email"],
            "password": wrong_password
        }

        with allure.step(f"Отправить запрос с неверным паролем: {wrong_password}"):
            response = send_auth_request(login_data)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == Messages.EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH

    @allure.title("Неуспешная авторизация без email")
    def test_missing_email_login(self):
        login_data = {
            "password": "some_password"
        }

        with allure.step("Отправить запрос без email"):
            response = send_auth_request(login_data)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == Messages.EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH

    @allure.title("Неуспешная авторизация с несуществующим email")
    @pytest.mark.parametrize("invalid_email", ["nonexistent@test.com", "invalid", ""])
    def test_invalid_email_login(self, invalid_email):
        login_data = {
            "email": invalid_email,
            "password": "some_password"
        }

        with allure.step(f"Отправить запрос с неверным email: {invalid_email}"):
            response = send_auth_request(login_data)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == Messages.EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH
    @allure.story("Неуспешная авторизация")
    @allure.title("Попытка авторизации с пустым JSON")
    def test_login_with_empty_json(self):
        with allure.step("Подготовить пустой JSON для запроса"):
            allure.attach(str(UserCreationData.PAYLOAD_EMPTY), name="Пустой JSON", attachment_type=allure.attachment_type.JSON)

        with allure.step("Отправить запрос на авторизацию с пустым телом"):
            login_data = UserCreationData.PAYLOAD_EMPTY
            response = send_auth_request(login_data)
            allure.attach(str(response.status_code), name="Код ответа")
            allure.attach(response.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 401, "Ожидается статус 401 для невалидного запроса"
            response_data = response.json()
            assert response_data["success"] is False, "Флаг успеха должен быть False"
            assert response_data["message"] == Messages.EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH, (
                f"Ожидаемое сообщение: '{Messages.EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH}', "
                f"Фактическое: '{response_data['message']}'"
            )




    @allure.story("Неуспешная авторизация удалённого пользователя")
    @allure.title("Попытка авторизации удалённого пользователя")
    def test_login_deleted_user(self):
        with allure.step("Зарегистрировать нового пользователя"):
            user_data = UserCreationData.PAYLOAD
            register_response = send_register_request(user_data)
            assert register_response.status_code == 200, f"Ошибка регистрации: {register_response.text}"
            token = register_response.json()['accessToken']
            time.sleep(1)  # Задержка после регистрации

        with allure.step("Удалить пользователя"):
            delete_response = delete_user(token)
            assert delete_response.status_code in [202], (
                f"Не удалось удалить пользователя: {delete_response.text}"
            )
            allure.attach(str(delete_response.status_code), name="Код ответа при удалении")
            allure.attach(delete_response.text, name="Тело ответа при удалении")
            time.sleep(1)  # Задержка после удаления

        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        with allure.step("Подготовить данные для авторизации удалённого пользователя"):
            allure.attach(str(login_data), name="Данные для входа", attachment_type=allure.attachment_type.JSON)

        with allure.step("Отправить запрос на авторизацию удалённого пользователя"):
            response = send_auth_request(login_data)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 401, "Ожидается статус 401 для удалённого пользователя"
            response_data = response.json()
            assert response_data["success"] is False, "Флаг успеха должен быть False"
            assert response_data["message"] == Messages.EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH, (
                f"Ожидаемое сообщение: '{Messages.EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH}', "
                f"Фактическое: '{response_data['message']}'"
            )