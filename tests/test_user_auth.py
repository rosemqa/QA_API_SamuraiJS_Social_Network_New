import allure
import pytest
from config.base_test import BaseTest
from config.data import AuthDataFirstUser
from services.auth.payloads import Payloads


@allure.epic('Authorization')
class TestUserAuth(BaseTest):

    excluded_params = [
        ("email", ["Please enter your Email"]),
        ("password", ["Enter your password"])
    ]

    wrong_credentials = [
        ("email", 'test@mail.com'),
        ("password", '123')
    ]

    @allure.description('Login with email and password, check if the current user is authorized, logout')
    def test_auth(self):
        # LOGIN USER
        login = self.api_auth.login_user()

        user_id_from_login = login['model'].data.userId
        assert user_id_from_login == AuthDataFirstUser.USER_ID, 'User ID in login response is not correct'
        auth_cookie = login['auth_cookie']

        # CHECK IS CURRENT USER AUTHORIZED
        authed_user = self.api_auth.is_user_auth(auth_cookie)

        assert authed_user.data.id == user_id_from_login, \
            'User ID from "login" method is not equal to user ID from "is user auth" method'
        assert authed_user.data.email == Payloads.login_data()['email'], \
            'Email from "login" method is not equal to email from "is user auth" method'
        assert authed_user.data.login == AuthDataFirstUser.USER_NAME, \
            'User name from "login" method is not equal to user name from "is user auth" method'

        # LOGOUT USER
        self.api_auth.logout_user()

    @allure.description('User cannot authorized without sending auth cookie')
    @allure.tag('negative')
    def test_authorization_without_auth_cookies(self):
        auth = self.api_auth.is_user_auth_without_auth_cookies()

        assert auth.messages == ['You are not authorized'], 'Check error message for not authed user'

    @allure.description('Unable to login with incorrect email format')
    @allure.tag('negative')
    @pytest.mark.parametrize('email', ['testmail.com', 'test@mailcom', 'test@.com', ])
    def test_login_with_incorrect_email_format(self, email):
        login = self.api_auth.login_with_incorrect_email_format(email)

        assert login.messages == ['Enter valid Email'], \
            'Error message for incorrect email format is not correct'
        assert login.fieldsErrors == [{'field': 'email', 'error': 'Enter valid Email'}], 'Check "fieldsErrors"'

    @allure.description('Cannot login if any required field (email or password) is empty')
    @allure.tag('negative')
    @pytest.mark.parametrize('empty_value, error_massage', excluded_params)
    def test_login_with_empty_field(self, empty_value, error_massage):
        login = self.api_auth.login_with_empty_field(empty_value)

        assert login.messages == error_massage, \
            f'Error message for empty {empty_value} field is not correct.'

    @allure.description('Cannot login if all required fields (email and password) are empty')
    @allure.tag('negative')
    def test_login_with_empty_fields(self):
        login = self.api_auth.login_with_empty_fields()

        assert login.messages == ['Please enter your Email', 'Enter your password'], \
            'Error message for empty required fields is not correct.'

    @allure.description('Cannot login with wrong email or password')
    @allure.tag('negative')
    @pytest.mark.parametrize('field, wrong_value', wrong_credentials)
    def test_login_with_wrong_credentials(self, field, wrong_value):
        login = self.api_auth.login_with_wrong_credentials(field, wrong_value)

        assert login.messages == ['Incorrect Email or Password'], \
            f'Error message for wrong {field} is not correct'
