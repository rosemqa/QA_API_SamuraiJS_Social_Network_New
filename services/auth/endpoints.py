from config.config import BASE_URL


class Endpoints:
    login = f'{BASE_URL}/auth/login'
    logout = f'{BASE_URL}/auth/logout'
    is_current_user_authorized = f'{BASE_URL}/auth/me'
