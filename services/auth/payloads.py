import os
from config.data import AuthDataFirstUser
from dotenv import load_dotenv

load_dotenv()


class Payloads:
    @staticmethod
    def login_data():
        return {
                "email": AuthDataFirstUser.LOGIN_DATA['email'],
                "password": f"{os.getenv('FIRST_PASSWORD')}",
                "rememberMe": True
            }
