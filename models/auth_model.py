from pydantic import BaseModel, field_validator
from uuid import UUID


class UserLogin(BaseModel):
    userId: int
    token: UUID


class LoginModel(BaseModel):
    data: UserLogin
    messages: list[str]
    fieldsErrors: list[str]
    resultCode: int


class UserAuthed(BaseModel):
    id: int
    login: str
    email: str


class AuthedModel(BaseModel):
    data: UserAuthed
    messages: list[str]
    fieldsErrors: list[str]
    resultCode: int


class LogoutModel(BaseModel):
    data: dict
    messages: list
    fieldsErrors: list
    resultCode: int

    @field_validator('data', 'messages', 'fieldsErrors', 'resultCode')
    def fields_are_empty(cls, value):
        if value:
            raise ValueError('Field is not empty')
        else:
            return value


class ErrorModel(BaseModel):
    data: dict
    messages: list
    fieldsErrors: list
    resultCode: int

    @field_validator('messages', 'resultCode')
    def fields_are_not_empty(cls, value):
        if not value:
            raise ValueError('Field is empty')
        else:
            return value
