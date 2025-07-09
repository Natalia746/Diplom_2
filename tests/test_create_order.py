import allure
import pytest
from common_test_methods import *
from data import *


@allure.feature('Создание заказа POST https://stellarburgers.nomoreparties.site/api/orders')
class TestCreateOrders:
    @allure.title('Успешное создание заказа с валидными ингредиентами')
    def test_create_order_success(self, registered_user, valid_ingredients):
        response = create_order(valid_ingredients, registered_user['token'])

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'order' in data
        assert 'number' in data['order']

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_empty_ingredients(self, registered_user):
        response = create_order([], registered_user['token'])

        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['message'] == Messages.MESSAGE_CREATE_ORDER_NO_INGREDIENTS

    @allure.title('Создание заказа с невалидным хэшем ингредиента')
    def test_create_order_invalid_hash(self, registered_user):
        response = create_order(['invalid_hash_123'], registered_user['token'])

        assert response.status_code == 500