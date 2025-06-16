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

    @allure.story("Неуспешная авторизация")
    @allure.title("Неуспешная авторизация зарегистрированного пользователя")
    @pytest.mark.parametrize("login_data,expected_message", [
        pytest.param(
            {"email": "registered_user['email']", "password": "wrong_password"},
            Messages.EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH,
            id="wrong_password"
        ),
        pytest.param(
            {"password": "some_password"},
            Messages.EXPECTED_MESSAGE_UNSUCCESSFUL_AUTH,
            id="missing_email"
        )
    ])
    def test_failed_login_scenarios(self, registered_user, login_data, expected_message):
        if "email" in login_data and login_data["email"] == "registered_user['email']":
            login_data["email"] = registered_user["email"]

        with allure.step(f"Отправить запрос с данными: {login_data}"):
            response = send_auth_request(login_data)

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == expected_message

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
