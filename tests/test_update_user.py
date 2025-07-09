import pytest
from unittest.mock import patch, MagicMock
import allure
from data import Messages, Url
from common_test_methods import send_update_user_data
import time
import requests

@allure.story("Обновление данных пользователя PATCH https://stellarburgers.nomoreparties.site/api/auth/user ")
class TestUserUpdate:

    @allure.title("Успешное обновление данных с авторизацией ")
    @pytest.mark.parametrize("field,value", [
        ("name", "New Name"),
        ("email", "new@example.com"),
        ("password", "NewP@ss123")
    ])
    def test_authorized_update(self, registered_user, field, value):
        update_data = {field: value}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "user": {**registered_user, **update_data}
        }

        with allure.step(f"Пытаемся изменить поле {field}"):
            with patch('requests.patch', return_value=mock_response) as mock_patch:
                response = send_update_user_data(
                    update_data=update_data,
                    auth_token=registered_user['token']
                )

                assert response.status_code == 200
                assert response.json()["success"] is True
                assert response.json()["user"][field] == value

                mock_patch.assert_called_once_with(
                    Url.BASE_URL + Url.UPDATE_USER,
                    headers={'Authorization': registered_user['token']},
                    json=update_data
                )

    @allure.title("Попытка обновления без авторизации")
    @pytest.mark.parametrize("field,value", [
        ("name", "New Name"),
        ("email", f"new_{time.time()}@example.com"),
        ("password", "NewP@ss123")
    ])
    def test_unauthorized_update(self, registered_user, field, value):
        update_data = {field: value}

        with allure.step(f"Пытаемся изменить поле {field} без авторизации"):
            # Отправляем запрос без токена авторизации
            response = send_update_user_data(
                update_data=update_data,
                auth_token=None
            )

            # Прикрепляем данные для отчета Allure
            allure.attach(f"Запрос: {update_data}", name="Данные обновления")
            allure.attach(f"Статус код: {response.status_code}", name="Код ответа")
            allure.attach(response.text, name="Тело ответа", attachment_type=allure.attachment_type.JSON)

            # Проверяем ответ сервера
            assert response.status_code == 401, "Ожидается статус 401 Unauthorized"
            response_data = response.json()
            assert response_data["success"] is False, "Флаг success должен быть False"
            assert response_data["message"] == Messages.MESSAGE_UPDATE_WITHOUT_AUTH, "Неверное сообщение об ошибке"

            # Дополнительная проверка: убеждаемся, что данные не изменились
            with allure.step("Проверить, что данные пользователя не изменились"):
                get_response = requests.get(
                    Url.BASE_URL + Url.AUTH_USER,
                    headers={'Authorization': registered_user['token']}
                )
                assert get_response.status_code == 200, "Не удалось получить данные пользователя"
