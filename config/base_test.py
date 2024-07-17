from services.auth.api_auth import AuthAPI
from services.users.api_users import UsersAPI


class BaseTest:
    def setup_method(self):
        self.api_auth = AuthAPI()
        self.api_users = UsersAPI()
