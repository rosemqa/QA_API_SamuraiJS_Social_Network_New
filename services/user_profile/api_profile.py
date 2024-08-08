import allure
import pytest
import requests

from config.config import Headers
from config.data import AuthDataFirstUser
from models.common_model import ResultModel, NotAuthModel, NegativeResultModel
from models.profile_model import ProfileModel, StatusModel, ProfilePhotosModel
from services.auth.api_auth import AuthAPI
from services.user_profile.endpoints import Endpoints
from services.user_profile.payloads import Payloads
from utils.helper import Helper
from utils.my_requests import MyRequests


# @pytest.fixture(scope='class')
# def login(request):
#     auth = AuthAPI()
#     request.cls.auth_cookie = auth.login_user()['auth_cookie']
#     yield


class ProfileAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.payloads = Payloads()

    def get_user_profile(self, user_id):
        response = MyRequests.get(
            url=self.endpoints.get_user_profile(user_id),
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ProfileModel(**response.json())
        return model

    @allure.step('Edit all profile data')
    def edit_user_profile(self, auth_cookie):
        payloads = self.payloads.edit_user_profile()
        response = MyRequests.put(
            url=self.endpoints.edit_user_profile,
            json=payloads,
            headers=self.headers.api_key,
            cookies={'.ASPXAUTH': auth_cookie},
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        ResultModel(**response.json())
        return payloads

    def edit_profile_contacts_with_incorrect_url_format(self, auth_cookie, contact, url):
        payloads = self.payloads.edit_user_profile()
        payloads['contacts'][contact] = url
        response = MyRequests.put(
            url=self.endpoints.edit_user_profile,
            json=payloads,
            headers=self.headers.api_key,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = NegativeResultModel(**response.json())
        return model

    @allure.step('Edit profile status')
    def edit_profile_status(self, auth_cookie):
        response = MyRequests.put(
            url=self.endpoints.edit_profile_status,
            headers=self.headers.api_key,
            json=self.payloads.edit_profile_status,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        ResultModel(**response.json())
        return self.payloads.edit_profile_status['status']

    @allure.step('Edit profile status without auth cookies')
    def edit_profile_status_without_auth_cookies(self):
        response = MyRequests.put(
            url=self.endpoints.edit_profile_status,
            headers=self.headers.api_key,
            json=self.payloads.edit_profile_status
        )
        assert response.status_code == 401, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = NotAuthModel(**response.json())
        return model

    @allure.step('Edit profile status with with too long (301 symbols) string')
    def edit_profile_status_with_too_long_string(self, auth_cookie):
        response = MyRequests.put(
            url=self.endpoints.edit_profile_status,
            headers=self.headers.api_key,
            json=self.payloads.long_status_string,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = NegativeResultModel(**response.json())
        return model

    @allure.step('Get profile status')
    def get_profile_status(self, user_id):
        response = MyRequests.get(
            url=self.endpoints.get_pofile_status(user_id),
            headers=self.headers.api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = StatusModel(response=response.json())
        return model.response

    @allure.step('Upload profile photo')
    def upload_profile_photo(self, auth_cookie):
        file = open('files/tiger.jpg', 'rb')
        response = requests.post(
            url=self.endpoints.edit_profile_photo,
            files={'file': file},
            headers=self.headers.api_key,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ProfilePhotosModel(**response.json())
        return model

    @allure.step('Update profile photo')
    def edit_profile_photo(self, auth_cookie):
        file = open('files/dog.jpg', 'rb')
        response = requests.put(
            url=self.endpoints.edit_profile_photo,
            files={'file': file},
            headers=self.headers.api_key,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ProfilePhotosModel(**response.json())
        return model

    @allure.step('Get profile photo content')
    def get_profile_photo_content(self, link):
        response = MyRequests.get(
            url=link
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        return response.content
