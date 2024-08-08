from config.config import BASE_URL


class Endpoints:
    edit_user_profile = f'{BASE_URL}/profile'
    get_user_profile = lambda self, user_id: f'{BASE_URL}/profile/{user_id}'
    get_pofile_status = lambda self, user_id: f'{BASE_URL}/profile/status/{user_id}'
    edit_profile_status = f'{BASE_URL}/profile/status'
    edit_profile_photo = f'{BASE_URL}/profile/photo'
