import requests
from config.data import AuthDataFirstUser
from services.auth.api_auth import AuthAPI
from services.user_profile.api_profile import ProfileAPI
from services.users.api_users import UsersAPI


class BaseTest:
    def setup_method(self):
        self.api_auth = AuthAPI()
        self.api_users = UsersAPI()
        self.api_profile = ProfileAPI()
