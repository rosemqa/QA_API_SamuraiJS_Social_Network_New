from services.auth.api_auth import AuthAPI
from services.dialogs.api_dialogs import DialogsAPI
from services.follow.api_follow import FollowAPI
from services.user_profile.api_profile import ProfileAPI
from services.users.api_users import UsersAPI


class BaseTest:
    def setup_method(self):
        self.api_auth = AuthAPI()
        self.api_users = UsersAPI()
        self.api_profile = ProfileAPI()
        self.api_follow = FollowAPI()
        self.api_dialogs = DialogsAPI()
