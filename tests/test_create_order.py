import allure
import pytest
from common_test_methods import *
from data import *


@allure.feature('Создание заказа POST https://stellarburgers.nomoreparties.site/api/orders')
class TestCreateOrders:
    @allure.title('Параметризованный тест создания заказа')
    @pytest.mark.parametrize(
        "ingredients_data, expected_status, expected_success, expected_message, check_order_number",
        [
            pytest.param(
                'valid',
                200,
                True,
                None,
                True,
                id="valid ingredients"
            ),
            pytest.param(
                [],
                400,
                False,
                Messages.MESSAGE_CREATE_ORDER_NO_INGREDIENTS,
                False,
                id="empty ingredients"
            ),
            pytest.param(
                ['invalid_hash_123'],
                500,
                None,
                None,
                False,
                id="invalid hash"
            ),
        ]
    )
    def test_create_order_parametrized(self,
            registered_user,
            ingredients_data,
            expected_status,
            expected_success,
            expected_message,
            check_order_number
    ):

        if ingredients_data == 'valid':
            ingredients_resp = get_ingredients()
            ingredients = [ingredient['_id'] for ingredient in ingredients_resp.json()['data'][:2]]
        else:
            ingredients = ingredients_data

        response = create_order(ingredients, registered_user['token'])

        assert response.status_code == expected_status

        if expected_status != 500:
            data = response.json()

            if expected_success is not None:
                assert data['success'] == expected_success

            # Проверяем сообщение об ошибке
            if expected_message is not None:
                assert data['message'] == expected_message

            # Проверяем наличие номера заказа
            if check_order_number:
                assert 'order' in data and 'number' in data['order']