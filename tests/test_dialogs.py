import random
import time
import allure
import pytest
from config.base_test import BaseTest
from config.config import BASE_URL
from config.data import AuthDataSecondUser, AuthDataFirstUser
from utils.my_requests import MyRequests


@allure.epic('Dialogs')
class TestDialogs(BaseTest):

    SENDER_ID = AuthDataFirstUser.USER_ID
    SENDER_NAME = AuthDataFirstUser.USER_NAME
    RECIPIENT_ID = AuthDataSecondUser.USER_ID

    @pytest.fixture(autouse=True)
    def logins(self):
        # LOGIN TO SENDER ACCOUNT
        response = MyRequests.post(f'{BASE_URL}/auth/login', json=AuthDataFirstUser.LOGIN_DATA)
        self.sender_auth_cookie = response.cookies['.ASPXAUTH']

        # LOGIN TO RECIPIENT ACCOUNT
        response = MyRequests.post(f'{BASE_URL}/auth/login', json=AuthDataSecondUser.LOGIN_DATA)
        self.recipient_auth_cookie = response.cookies['.ASPXAUTH']

    @allure.description(
        'The sender can send a message and the recipient can receive it, the message is marked as viewed after viewing'
    )
    def test_send_message(self, check):
        # SEND MESSAGE
        send = self.api_dialogs.send_message(self.RECIPIENT_ID, self.sender_auth_cookie)
        message_id = send.data.message.id
        with check:
            assert send.data.message.senderId == self.SENDER_ID, \
                'Sender ID in the post response does not match the sender ID'
        with check:
            assert send.data.message.senderName == self.SENDER_NAME, \
                'Sender name in the post response does not match the sender name'
        with check:
            assert send.data.message.recipientId == self.RECIPIENT_ID, \
                'Recipient ID in the post response does not match the Recipient ID'

        # GET LIST OF MESSAGES RECEIVED BY RECIPIENT
        receive = self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie)
        with check:
            assert receive.items[-1].id == message_id, 'Message ID in the get and post responses is different'
        with check:
            assert receive.items[-1].body == send.data.message.body, \
                'Message text in the get and post responses is different'
        with check:
            assert receive.items[-1].senderId == self.SENDER_ID, \
                'Sender ID in the get response does not match the sender ID'
        with check:
            assert receive.items[-1].senderName == self.SENDER_NAME, \
                'Sender name in the get response does not match the sender name'
        with check:
            assert receive.items[-1].recipientId == send.data.message.recipientId, \
                'Recipient ID in the get response does not match the recipient ID'
        with check:
            assert receive.items[-1].addedAt == send.data.message.addedAt, \
                'Time in the get and post responses is different'

        # CHECK IF SENT MESSAGE HAS BEEN VIEWED
        view = self.api_dialogs.is_message_viewed(message_id, self.sender_auth_cookie)
        assert view is True, 'The sent message was not marked as viewed for sender'

    @allure.description('Number of new messages is correct after sending/viewing them')
    def test_new_messages_count(self):
        # GET INITIAL COUNT OF NEW MESSAGES
        initial_count = self.api_dialogs.get_new_messages_count(self.recipient_auth_cookie)
        print(initial_count)

        # SEND A FEW MESSAGES (2-5)
        number_of_messages_to_send = random.randint(2, 5)
        for _ in range(number_of_messages_to_send):
            self.api_dialogs.send_message(self.RECIPIENT_ID, self.sender_auth_cookie)

        # GET COUNT OF NEW MESSAGES AFTER SENDING THEM
        count = self.api_dialogs.get_new_messages_count(self.recipient_auth_cookie)
        print(count)
        assert count == initial_count + number_of_messages_to_send, 'New messages count is not correct after sending'

        # GET LIST OF RECEIVED MESSAGES (VIEW ALL MESSAGES)
        self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie)

        # GET COUNT OF NEW MESSAGES AFTER VIEWING THEM
        count = self.api_dialogs.get_new_messages_count(self.recipient_auth_cookie)
        print(count)
        assert count == initial_count, 'New messages count is not correct after viewing'

    @allure.description('The message can be deleted and restored by recipient')
    def test_delete_and_restore_message(self):
        # SEND MESSAGE
        send = self.api_dialogs.send_message(self.RECIPIENT_ID, self.sender_auth_cookie)
        message_id = send.data.message.id

        # DELETE MESSAGE BY RECIPIENT
        self.api_dialogs.delete_message(message_id, self.recipient_auth_cookie)

        # GET LIST OF RECEIVED MESSAGES
        receive = self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie)
        assert message_id not in [message.id for message in receive.items], 'Message was not deleted'

        # RESTORE MESSAGE FROM DELETED
        self.api_dialogs.restore_message(message_id, self.recipient_auth_cookie)

        # GET LIST OF RECEIVED MESSAGES
        receive = self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie)
        assert message_id in [message.id for message in receive.items], \
            'Message was not restored from the deleted ones'

    @allure.description('The message can be placed to spam and than restored')
    def test_place_message_to_spam(self):
        # SEND MESSAGE
        send = self.api_dialogs.send_message(self.RECIPIENT_ID, self.sender_auth_cookie)
        message_id = send.data.message.id

        # PLACE MESSAGE TO SPAM
        self.api_dialogs.add_message_to_spam(message_id, self.recipient_auth_cookie)

        # GET LIST OF RECEIVED MESSAGES
        receive = self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie)
        assert message_id not in [message.id for message in receive.items], \
            'Message was not restored from the deleted ones'

        # RESTORE MESSAGE FROM SPAM
        self.api_dialogs.restore_message(message_id, self.recipient_auth_cookie)

        # GET LIST OF RECEIVED MESSAGES
        receive = self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie)
        assert message_id in [message.id for message in receive.items], \
            'Message was not restored from spam'

    @allure.description('The messages can be filtered by date (return messages newer than specified date)')
    def test_filtering_messages_by_date(self):
        # SEND 5 MESSAGES AND GET A LIST OF THEIR SENDING DATES
        date_list = []
        for _ in range(5):
            send = self.api_dialogs.send_message(self.RECIPIENT_ID, self.sender_auth_cookie)
            date = send.data.message.addedAt
            date_list.append(date)
            time.sleep(1)

        # GET MESSAGES NEWER THAN DATE SPECIFIED (2 last messages out of 5)
        date = date_list[2]  # date of third message out of 5
        message_list = self.api_dialogs.get_messages_newer_than_date(self.SENDER_ID, date, self.recipient_auth_cookie)

        assert len(message_list) == 2, 'Incorrect number of filtered messages'

        assert date_list[-2:] == [message.addedAt for message in message_list], \
            'Dates of filtered messages are incorrect'

    @allure.description('The user can get a list of all dialogs and start chatting with any user from the list')
    def test_all_dialogs(self, logins):
        # GET ALL DIALOGS LIST AND GET ID OF THE FIRST DIALOG
        dialogs = self.api_dialogs.get_all_dialogs(self.sender_auth_cookie)
        initial_first_dialog = dialogs[0].id

        # CHOOSE A RANDOM DIALOG EXCEPT THE FIRST AND GET ITS ID
        list_length = len(dialogs)
        random_dialog = dialogs[random.randint(1, list_length - 1)].id

        assert initial_first_dialog != random_dialog, 'All dialog IDs in the list are the same'

        # PLACE A RANDOM DIALOG AT THE TOP OF THE LIST (START CHATTING)
        self.api_dialogs.start_chatting(random_dialog, self.sender_auth_cookie)

        # GET ALL DIALOGS LIST AND GET ID OF THE FIRST DIALOG
        dialogs = self.api_dialogs.get_all_dialogs(self.sender_auth_cookie)
        new_first_dialog = dialogs[0].id

        assert new_first_dialog == random_dialog, 'The selected dialog was not placed at the top of the list'

    @allure.description('Can select the length of the message list')
    def test_message_list_of_sertan_length(self):
        # SELECT RANDOM LENGTH (1-20) OF THE MESSAGE LIST
        list_length = random.randint(1, 20)

        # GET THE MESSAGE LIST OF THE SELECTED LENGTH
        message_list = self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie, count=list_length)

        # CHECK THE LIST LENGTH
        assert len(message_list.items) == list_length, 'Message list length does not match the selected length'

        # GET THE MESSAGE LIST OF DEFAULT LENGTH (10) AND CHECK ITS LENGTH
        default_list = self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie)

        assert len(default_list.items) == 10, 'The default message list length is not 10 '

    @allure.description('Can select the page of the message list')
    def test_message_list_pages(self):
        # GET THE FIRST PAGE OF THE LIST AND GET ID OF THE FIRST MESSAGE
        first_page = self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie)
        first_page_message_id = first_page.items[0].id

        # GET THE SECOND PAGE OF THE LIST AND GET ID OF THE FIRST MESSAGE
        second_page = self.api_dialogs.get_message_list(self.SENDER_ID, self.recipient_auth_cookie, page=2)
        second_page_message_id = second_page.items[0].id

        assert first_page_message_id != second_page_message_id, 'The list page was not changed'
