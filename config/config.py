import os
from dotenv import load_dotenv

load_dotenv()


BASE_URL = 'https://social-network.samuraijs.com/api/1.0'


class Headers:
    api_key = {"API-KEY": f"{os.getenv('FIRST_API_KEY')}"}
    second_user_api_key = {"API-KEY": f"{os.getenv('SECOND_API_KEY')}"}
