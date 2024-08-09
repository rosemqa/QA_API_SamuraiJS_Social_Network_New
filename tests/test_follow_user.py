import allure
from config.base_test import BaseTest
from config.data import AuthDataSecondUser


@allure.epic('Follow user')
class TestFollowUser(BaseTest):
    @allure.description('User can follow/unfollow another user')
    def test_follow_user(self, login):
        requested_user_id = AuthDataSecondUser.USER_ID

        # FOLLOW REQUESTED USER
        self.api_follow.follow_user_by_id(requested_user_id, self.auth_cookie)

        # IS CURRENT USER FOLLOWER FOR REQUESTED USER
        is_follow = self.api_follow.is_user_followed(requested_user_id, self.auth_cookie)
        assert is_follow is True, 'User has not followed'

        # UNFOLLOW REQUESTED USER
        self.api_follow.unfollow_user_by_id(requested_user_id, self.auth_cookie)

        # IS CURRENT USER FOLLOWER FOR REQUESTED USER
        is_follow = self.api_follow.is_user_followed(requested_user_id, self.auth_cookie)
        assert is_follow is False, 'User has not unfollowed'

    @allure.description('Check the error message when unfollowing from already unfollowed user')
    def test_unfollow_unfollowed_user(self, login):
        unfollowed_user_id = AuthDataSecondUser.USER_ID

        unfollow = self.api_follow.unfollow_unfollowed_user(unfollowed_user_id, self.auth_cookie)
        assert unfollow.messages == ['You are already unfollowed this user'], \
            'Wrong response message when unfollowing from an unfollowed user'

    @allure.description('cHECK THE error message when following to an already followed user')
    def test_follow_user_twice(self, login):
        follow = self.api_follow.follow_user_twice(self.auth_cookie)

        assert follow.messages == ['You are already following this user'], \
            'Wrong response message when following to an already followed user'
