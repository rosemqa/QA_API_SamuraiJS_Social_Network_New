from config.config import BASE_URL


class Endpoints:
    get_follow_user = lambda self, user_id: f'{BASE_URL}/follow/{user_id}'
    follow_user_by_id = lambda self, user_id: f'{BASE_URL}/follow/{user_id}'
    unfollow_user = lambda self, user_id: f'{BASE_URL}/follow/{user_id}'
