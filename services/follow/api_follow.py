import allure
from config.config import Headers
from models.common_model import ResultModel, NegativeResultModel
from models.follow_model import IsFollowModel
from services.follow.endpoints import Endpoints
from utils.helper import Helper
from utils.my_requests import MyRequests


class FollowAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step('Check if you are following a user by id')
    def is_user_followed(self, user_id, auth_cookie):
        response = MyRequests.get(
            url=self.endpoints.get_follow_user(user_id),
            headers=self.headers.api_key,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = IsFollowModel(response=response.json())
        return model.response

    @allure.step('Follow a user by id')
    def follow_user_by_id(self, user_id, auth_cookie):
        response = MyRequests.post(
            url=self.endpoints.follow_user_by_id(user_id),
            cookies={'.ASPXAUTH': auth_cookie},
            headers=self.headers.api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ResultModel(**response.json())
        return model

    @allure.step('Unfollow a user by id')
    def unfollow_user_by_id(self, user_id, auth_cookie):
        response = MyRequests.delete(
            url=self.endpoints.unfollow_user(user_id),
            cookies={'.ASPXAUTH': auth_cookie},
            headers=self.headers.api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ResultModel(**response.json())
        return model

    @allure.step('Unfollow from already unfollowed user')
    def unfollow_unfollowed_user(self, user_id, auth_cookie):
        response = MyRequests.delete(
            url=self.endpoints.unfollow_user(user_id),
            cookies={'.ASPXAUTH': auth_cookie},
            headers=self.headers.api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = NegativeResultModel(**response.json())
        return model

    @allure.step('Follow a user twice')
    def follow_user_twice(self, auth_cookie):
        followed_user_id = 30700  # user should be already followed
        response = MyRequests.post(
            url=self.endpoints.follow_user_by_id(followed_user_id),
            cookies={'.ASPXAUTH': auth_cookie},
            headers=self.headers.api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = NegativeResultModel(**response.json())
        return model
