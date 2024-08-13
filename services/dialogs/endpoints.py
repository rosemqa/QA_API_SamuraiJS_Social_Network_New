from config.config import BASE_URL


class Endpoints:
    start_chatting = lambda self, user_id: f'{BASE_URL}/dialogs/{user_id}'
    get_all_dialogs = f'{BASE_URL}/dialogs'
    get_message_list = lambda self, user_id: f'{BASE_URL}/dialogs/{user_id}/messages'
    send_message = lambda self, user_id: f'{BASE_URL}/dialogs/{user_id}/messages'
    is_message_viewed = lambda self, message_id: f'{BASE_URL}/dialogs/messages/{message_id}/viewed'
    add_message_to_spam = lambda self, message_id: f'{BASE_URL}/dialogs/messages/{message_id}/spam'
    delete_message = lambda self, message_id: f'{BASE_URL}/dialogs/messages/{message_id}'
    restore_message = lambda self, message_id: f'{BASE_URL}/dialogs/messages/{message_id}/restore'
    get_messages_newer_than_date = lambda self, user_id, date: \
        f'{BASE_URL}/dialogs/{user_id}/messages/new?newerThen={date}'
    get_new_messages_count = f'{BASE_URL}/dialogs/messages/new/count'
