from services.auth.api_auth import AuthAPI


class BaseTest:
    def setup_method(self):
        self.api_auth = AuthAPI()
