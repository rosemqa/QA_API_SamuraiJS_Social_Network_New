import allure
from config.config import Headers
from models.common_model import ResultModel
from models.dialogs_model import AllDialogsModel, DialogsListItem, MessageListModel, SendMessageModel, \
    IsMessageViewedModel, PostMessageDetails, NewMessagesCountModel
from services.dialogs.endpoints import Endpoints
from services.dialogs.payloads import Payloads
from utils.helper import Helper
from utils.my_requests import MyRequests


class DialogsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.payloads = Payloads()

    @allure.step('Start chatting, refresh your companion so that he was at the top of the all_dialogs list')
    def start_chatting(self, user_id, auth_cookie):
        response = MyRequests.put(
            url=self.endpoints.start_chatting(user_id),
            cookies={'.ASPXAUTH': auth_cookie},
            headers=self.headers.api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ResultModel(**response.json())
        return model

    @allure.step('Get list of all dialogs')
    def get_all_dialogs(self, auth_cookie):
        response = MyRequests.get(
            url=self.endpoints.get_all_dialogs,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = [DialogsListItem(**item) for item in response.json()]
        # model = AllDialogsModel(response=response.json())
        return model

    @allure.step('Get list of messages with your friend')
    def get_message_list(self, user_id, auth_cookie, count=None, page=None):
        response = MyRequests.get(
            url=self.endpoints.get_message_list(user_id) + f'?count={count}&page={page}',
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = MessageListModel(**response.json())
        return model

    @allure.step('Send message to your friend')
    def send_message(self, user_id, auth_cookie):
        response = MyRequests.post(
            url=self.endpoints.send_message(user_id),
            cookies={'.ASPXAUTH': auth_cookie},
            headers=self.headers.api_key,
            json=self.payloads.send_message
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = SendMessageModel(**response.json())
        return model

    @allure.step('Check if your message viewed')
    def is_message_viewed(self, message_id, auth_cookie):
        response = MyRequests.get(
            url=self.endpoints.is_message_viewed(message_id),
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = IsMessageViewedModel(response=response.json())
        return model.response

    @allure.step('Add message to spam by message ID')
    def add_message_to_spam(self, message_id, auth_cookie):
        response = MyRequests.post(
            url=self.endpoints.add_message_to_spam(message_id),
            cookies={'.ASPXAUTH': auth_cookie},
            headers=self.headers.second_user_api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ResultModel(**response.json())
        return model

    @allure.step('Delete message by message ID')
    def delete_message(self, message_id, auth_cookie):
        response = MyRequests.delete(
            url=self.endpoints.delete_message(message_id),
            cookies={'.ASPXAUTH': auth_cookie},
            headers=self.headers.second_user_api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ResultModel(**response.json())
        return model

    @allure.step('Restore your message form deleted or spam')
    def restore_message(self, message_id, auth_cookie):
        response = MyRequests.put(
            url=self.endpoints.restore_message(message_id),
            cookies={'.ASPXAUTH': auth_cookie},
            headers=self.headers.second_user_api_key
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = ResultModel(**response.json())
        return model

    @allure.step('Get messages newer than certain date')
    def get_messages_newer_than_date(self, user_id, date, auth_cookie):
        response = MyRequests.get(
            url=self.endpoints.get_messages_newer_than_date(user_id, date),
            headers=self.headers.api_key,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = [PostMessageDetails(**item) for item in response.json()]
        return model

    @allure.step('Get the number of new messages')
    def get_new_messages_count(self, auth_cookie):
        response = MyRequests.get(
            url=self.endpoints.get_new_messages_count,
            cookies={'.ASPXAUTH': auth_cookie}
        )
        assert response.status_code == 200, f'{response.status_code} {response.text}'
        self.attach_response(response.json())
        model = NewMessagesCountModel(response=response.json())
        return model.response
