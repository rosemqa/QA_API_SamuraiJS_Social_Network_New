import allure
from config.config import Headers
from models.auth_model import LoginModel, AuthedModel, LogoutModel, ErrorModel
from services.auth.endpoints import Endpoints
from services.auth.payloads import Payloads
from utils.helper import Helper
from utils.my_requests import MyRequests


class AuthAPI(Helper):
    def __init__(self):
        super().__init__()
        self.endpoints = Endpoints()
        self.payloads = Payloads()
        self.headers = Headers()

    @allure.step('Login user')
    def login_user(self):
        response = MyRequests.post(
            url=self.endpoints.login,
            json=self.payloads.login_data(),
            headers=self.headers.api_key
        )
        auth_cookie = response.cookies['.ASPXAUTH']
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = LoginModel(**response.json())
        return {'model': model, 'auth_cookie': auth_cookie}

    @allure.step('Is current user authorized')
    def is_user_auth(self, auth_cookie):
        response = MyRequests.get(
            url=self.endpoints.is_current_user_authorized,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.content.decode()}'
        self.attach_response(response.json())
        model = AuthedModel(**response.json())
        return model

    @allure.step('Is current user authorized without auth cookies')
    def is_user_auth_without_auth_cookies(self):
        response = MyRequests.get(
            url=self.endpoints.is_current_user_authorized
        )
        assert response.status_code == 200, f'{response.status_code} {response.content.decode()}'
        self.attach_response(response.json())
        model = ErrorModel(**response.json())
        return model

    @allure.step('Logout user')
    def logout_user(self):
        response = MyRequests.post(
            url=self.endpoints.logout,
            headers=self.headers.api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = LogoutModel(**response.json())
        return model

    @allure.step('Login with incorrect email format')
    def login_with_incorrect_email_format(self, email):
        payload = self.payloads.login_data()
        payload['email'] = email
        response = MyRequests.post(
            url=self.endpoints.login,
            json=payload,
            headers=self.headers.api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ErrorModel(**response.json())
        return model

    @allure.step('Login with empty required field')
    def login_with_empty_field(self, empty_value):
        payload = self.payloads.login_data()
        payload.update({empty_value: ''})
        response = MyRequests.post(
            url=self.endpoints.login,
            headers=self.headers.api_key,
            json=payload
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ErrorModel(**response.json())
        return model

    @allure.step('Login with all empty required fields')
    def login_with_empty_fields(self):
        payload = self.payloads.login_data()
        payload.update({'email': ''})
        payload.update({'password': ''})
        response = MyRequests.post(
            url=self.endpoints.login,
            headers=self.headers.api_key,
            json=payload
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ErrorModel(**response.json())
        return model

    @allure.step('Login with wrong email or password')
    def login_with_wrong_credentials(self, field, wrong_value):
        payload = self.payloads.login_data()
        payload[field] = wrong_value
        response = MyRequests.post(
            url=self.endpoints.login,
            headers=self.headers.api_key,
            json=payload,
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ErrorModel(**response.json())
        return model
