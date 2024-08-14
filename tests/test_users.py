import random
import allure
import pytest
from config.base_test import BaseTest


@allure.epic('Users')
class TestUsers(BaseTest):
    @allure.description('Get list of available users by default (w/o any params)')
    def test_get_user_list_by_default(self):
        page_size_by_default = 10   # how many items (users) will be returned in response

        users = self.api_users.get_user_list_by_default()
        number_of_users_per_page = len(users.items)

        assert number_of_users_per_page == page_size_by_default, \
            'Number of users on the page is not equal to the page size by default'

    @allure.description('Get list of available users with custom params (with the specified page size)')
    @pytest.mark.parametrize('page_size', [1, 20, 100])
    def test_get_custom_users_list(self, page_size):
        users = self.api_users.get_custom_users_list(page_size=page_size)
        number_of_users_per_page = len(users.items)

        assert number_of_users_per_page == page_size, \
            'Number of users on the page is not equal to the specified page size'

    @allure.description('Get too long users list (with page size more than 100 items)')
    @allure.tag('negative')
    def test_get_too_long_users_list(self):
        page_size = 101

        users = self.api_users.get_too_long_users_list(page_size)

        assert users.error == 'Max page size is 100 items', \
            'Check error message for too long user list'

    @allure.description('Check the user lists on different pages are not the same')
    def test_get_users_list_by_page_number(self):
        # GET USER ID OF FIRST USER FROM FIRST PAGE
        first_page = self.api_users.get_custom_users_list(page_number=1)
        user_id_from_first_page = first_page.items[0].id

        # GET USER ID OF FIRST USER FROM SECOND PAGE
        second_page = self.api_users.get_custom_users_list(page_number=2)
        user_id_from_second_page = second_page .items[0].id

        assert user_id_from_first_page != user_id_from_second_page, \
            'User IDs on two different pages are the same, probably page number has not changed'

    @allure.description('Test get users list filtered by username')
    def test_get_user_by_term(self):
        number_of_users_with_specified_name = 1

        # GET USER LIST AND SELECT ANY RANDOM USER
        users = self.api_users.get_user_list_by_default()
        user_name = users.items[random.randint(0, 9)].name

        # GET USER LIST WITH SPECIFIED USER NAME
        user = self.api_users.get_user_by_term(user_name)

        assert user.items[0].name == user_name, 'Check user name'
        assert len(user.items) == number_of_users_with_specified_name, 'Check length of the filtered user list'
        assert user.totalCount == number_of_users_with_specified_name, 'Check total count'
