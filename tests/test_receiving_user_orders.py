import allure
import pytest
from common_test_methods import *
from data import *
from unittest.mock import patch, Mock

@allure.feature('Заказы пользовател GET https://stellarburgers.nomoreparties.site/api/orders')
class TestUserOrders:

    @allure.title('Получение заказов без авторизации')
    def test_get_orders_unauthorized(self):
        response = get_user_orders()
        assert response.status_code == 401
        assert response.json()['message'] == Messages.MESSAGE_GET_ORDERS_UNAUTHORIZED

    @allure.title('Получение заказов с авторизацией')
    @patch('common_test_methods.get_ingredients')
    def test_get_orders_authorized(self,mock_get_ingredients, registered_user):
        #  Мокируем ответ с ингредиентами с использованием Mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data":
                Ingredients.MOCK_INGREDIENTS

        }
        mock_get_ingredients.return_value = mock_response

        valid_ingredients = Ingredients.VALID_INGREDIENTS

        create_response = create_order(valid_ingredients, registered_user['token'])
        assert create_response.status_code == 200
        create_data = create_response.json()
        order_number = create_data['order']['number']

        response = get_user_orders(registered_user['token'])
        data = response.json()

        assert response.status_code == 200
        assert data['success'] is True
        assert isinstance(data['orders'], list)
        assert len(data['orders']) > 0
        assert all(key in data for key in ['total', 'totalToday'])

        #  Проверка наличия созданного заказа в списке
        created_order = next(
            (order for order in data['orders'] if order['number'] == order_number),
            None
        )
        assert created_order is not None, "Созданный заказ не найден в списке"

        # Проверка деталей заказа
        assert created_order['ingredients'] == valid_ingredients
        assert created_order['status'] in ['created', 'pending', 'done']
        assert 'createdAt' in created_order
        assert 'updatedAt' in created_order