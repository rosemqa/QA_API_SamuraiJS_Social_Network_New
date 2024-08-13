import pytest
from services.auth.api_auth import AuthAPI


@pytest.fixture(scope='class')
def login(request):
    """Login and get auth cookie"""
    auth = AuthAPI()
    request.cls.auth_cookie = auth.login_user()['auth_cookie']
