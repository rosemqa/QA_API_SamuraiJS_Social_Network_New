import os
from dotenv import load_dotenv

load_dotenv()


class Payloads:
    @staticmethod
    def login_data():
        return {
                "email": "gilis87832@lanxi8.com",
                "password": f"{os.getenv('FIRST_PASSWORD')}",
                "rememberMe": True
            }
