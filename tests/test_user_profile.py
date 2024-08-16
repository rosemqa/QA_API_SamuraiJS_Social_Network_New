import allure
import pytest
from config.base_test import BaseTest
from config.data import AuthDataFirstUser


@allure.epic('User profile')
class TestUserProfile(BaseTest):

    contacts = [
        ("facebook", 'https://facebook#com'),
        ("website", 'https://website#com'),
        ("vk", 'https://vk#com'),
        ("twitter", 'https://twitter#com'),
        ("instagram", 'https://instagram#com'),
        ("youtube", 'https://youtube#com'),
        ("github", 'https://github#com'),
        ("mainLink", 'https://mainLink#com')
    ]

    @allure.description('Can edit profile status and get status')
    def test_edit_status(self, log_in):
        # EDIT STATUS
        new_status = self.api_profile.edit_profile_status(self.auth_cookie)

        # GET STATUS
        edited_status = self.api_profile.get_profile_status(AuthDataFirstUser.USER_ID)

        assert edited_status == new_status, 'Profile status has not changed'

    @allure.description('Not auth user cannot edit their profile status')
    @allure.tag('negative')
    def test_edit_user_status_not_auth(self):
        self.api_profile.edit_profile_status_without_auth_cookies()

    @allure.description('Unable to edit profile status if the string length exceeds 300 characters')
    @allure.tag('negative')
    def test_edit_user_status_with_too_long_string(self, log_in):
        status = self.api_profile.edit_profile_status_with_too_long_string(self.auth_cookie)
        assert status.messages == ['Max Status length is 300 symbols']

    @allure.description('Can edit all profile data')
    def test_edit_user_profile(self, log_in, check):
        # EDIT PROFILE DATA
        new_profile_data = self.api_profile.edit_user_profile(self.auth_cookie)

        about_me = new_profile_data['aboutMe']
        looking_for_job = new_profile_data['lookingForAJob']
        job_description = new_profile_data['lookingForAJobDescription']
        full_name = new_profile_data['fullName']
        contacts = new_profile_data['contacts']

        # GET PROFILE DATA
        edited_profile_data = self.api_profile.get_user_profile(AuthDataFirstUser.USER_ID)

        with check:
            assert about_me == edited_profile_data.aboutMe, 'Check "aboutMe" in the Get response'
        with check:
            assert looking_for_job == edited_profile_data.lookingForAJob, 'Check "lookingForAJob" in the Get response'
        with check:
            assert job_description == edited_profile_data.lookingForAJobDescription, \
                'Check "lookingForAJobDescription" in the Get response'
        with check:
            assert full_name == edited_profile_data.fullName, 'Check "fullName" in the Get response'

        for contact, value in contacts.items():
            with check:
                assert value == str(edited_profile_data.contacts.model_dump()[contact]), \
                    f'Check "{contact}" in the Get response'

    @allure.description('Profile contacts cannot be edited with incorrect url format')
    @allure.tag('negative')
    @pytest.mark.parametrize('contact, url', contacts)
    def test_edit_profile_contacts_with_incorrect_url_format(self, log_in, contact, url):
        result = self.api_profile.edit_profile_contacts_with_incorrect_url_format(self.auth_cookie, contact, url)

        assert result.messages == [f'Invalid url format (Contacts->{contact[0].upper() + contact[1:]})']

    @allure.description('Can upload and update profile photo')
    def test_profile_photo(self, log_in, check):
        user_id = AuthDataFirstUser.USER_ID
        # UPLOAD PHOTO
        upload_photo = self.api_profile.upload_profile_photo(self.auth_cookie)

        small_photo_link = upload_photo.data.photos.small
        large_photo_link = upload_photo.data.photos.large

        with check:
            assert f'/activecontent/images/users/{user_id}/user-small.jpg' in str(small_photo_link), \
                'Small image link is not correct'
        with check:
            assert f'/activecontent/images/users/{user_id}/user.jpg' in str(large_photo_link), \
                'Large image link is not correct'

        # GET PHOTOS
        original_small_photo = self.api_profile.get_profile_photo_content(small_photo_link)
        with check:
            assert original_small_photo[:2] == b'\xff\xd8', 'File is not a small JPEG image'

        original_large_photo = self.api_profile.get_profile_photo_content(large_photo_link)
        with check:
            assert original_large_photo[:2] == b'\xff\xd8', 'File is not a large JPEG image'

        # UPLOAD NEW PHOTO (EDIT PHOTO)
        self.api_profile.edit_profile_photo(self.auth_cookie)

        # GET NEW PHOTOS
        new_small_photo = self.api_profile.get_profile_photo_content(small_photo_link)
        new_large_photo = self.api_profile.get_profile_photo_content(large_photo_link)

        with check:
            assert original_small_photo != new_small_photo, 'Small photo has not changed'
        assert original_large_photo != new_large_photo, 'Large photo has not changed'
