from wsgiref.headers import Headers
import allure
from models.users_model import UserListPositiveModel, UserListNegativeModel
from services.users.endpoints import Endpoints
from utils.helper import Helper
from utils.my_requests import MyRequests


class UsersAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step('Get list of available users by default (w/o any params)')
    def get_user_list_by_default(self):
        response = MyRequests.get(
            url=self.endpoints.get_user_list,
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = UserListPositiveModel(**response.json())
        return model

    @allure.step('Get list of available users with the specified page size')
    def get_custom_users_list(self, page_size=None, page_number=None):
        params = {
            'count': page_size,
            'page': page_number
        }
        response = MyRequests.get(
            url=self.endpoints.get_user_list,
            params=params
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = UserListPositiveModel(**response.json())
        return model

    @allure.step('Get list of available users with the specified page size')
    def get_too_long_users_list(self, page_size):
        params = {'count': page_size}
        response = MyRequests.get(
            url=self.endpoints.get_user_list,
            params=params
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = UserListNegativeModel(**response.json())
        return model

    @allure.step('Get users list filtered by username')
    def get_user_by_term(self, term):
        params = {'term': term}
        response = MyRequests.get(
            url=self.endpoints.get_user_list,
            params=params
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = UserListPositiveModel(**response.json())
        return model
