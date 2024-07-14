import os
from dotenv import load_dotenv

load_dotenv()


class AuthDataFirstUser:
    LOGIN_DATA = {
            "email": "gilis87832@lanxi8.com",
            "password": f"{os.getenv('FIRST_PASSWORD')}",
            "rememberMe": True
        }
    API_KEY = {"API-KEY": f"{os.getenv('FIRST_API_KEY')}"}
    USER_NAME = 'FanLis'
    USER_ID = 30478


class AuthDataSecondUser:
    LOGIN_DATA = {
        "email": "vogopo7321@wenkuu.com",
        "password": f"{os.getenv('SECOND_PASSWORD')}",
        "rememberMe": True
    }
    API_KEY = {"API-KEY": f"{os.getenv('SECOND_API_KEY')}"}
    USER_NAME = 'NufNuf'
    USER_ID = 30563
