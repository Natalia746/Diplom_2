import allure
import requests
from data import Url


@allure.title("Отправка запроса авторизации пользователя")
def send_auth_request(login_data):
    with allure.step("Отправка запроса на авторизацию"):
        url = Url.BASE_URL + Url.AUTH_USER
        response = requests.post(url, json=login_data)
        return response

@allure.title("Отправка запроса регистрации пользователя")
def  send_register_request(test_data):
    with allure.step("Отправить запрос на регистрацию"):
        response = requests.post(
            Url.BASE_URL + Url.REGISTER,
            json=test_data
        )
        allure.attach(str(response.status_code), name="Код ответа")
        allure.attach(response.text, name="Тело ответа")
        return response


@allure.title("Отправка запроса для обновления данных пользователя")
def send_update_user_data(update_data, auth_token=None):
    with allure.step("Отправить запрос на обновление"):
        headers = {}
        if auth_token:
            headers['Authorization'] = auth_token

        response = requests.patch(
            Url.BASE_URL + Url.UPDATE_USER,
            headers=headers,
            json=update_data
        )
        return response


@allure.title("Получение заказов пользователя")
def get_user_orders(auth_token=None):
    headers = {}
    if auth_token:
        headers['Authorization'] = auth_token
    with allure.step("Отправка запроса на получение заказов"):
        response = requests.get(
            Url.BASE_URL + Url.ORDERS,
            headers=headers
        )
        allure.attach(str(response.status_code), name="Код ответа")
        allure.attach(response.text, name="Тело ответа")
        return response

@allure.title("Получение списка ингредиентов")
def get_ingredients():
    with allure.step("Запрос списка ингредиентов"):
        response = requests.get(Url.BASE_URL + Url.INGREDIENTS)
        allure.attach(str(response.status_code), name="Код ответа")
        return response


@allure.title("Создание заказа")
def create_order(ingredients, auth_token=None):
    headers = {}
    if auth_token:
        headers['Authorization'] = auth_token
    payload = {"ingredients": ingredients}
    with allure.step("Отправка запроса на создание заказа"):
        response = requests.post(
            Url.BASE_URL + Url.ORDERS,
            headers=headers,
            json=payload
        )
        allure.attach(str(response.status_code), name="Код ответа")
        allure.attach(response.text, name="Тело ответа")
        return response


@allure.title("Удаление пользователя")
def delete_user(auth_token):
    with allure.step("Отправка запроса на удаление пользователя"):
        response = requests.delete(
            Url.BASE_URL + Url.DELETE_USER,
            headers={'Authorization': auth_token}
        )
        allure.attach(str(response.status_code), name="Код ответа при удалении")
        allure.attach(response.text, name="Тело ответа при удалении")
        return response