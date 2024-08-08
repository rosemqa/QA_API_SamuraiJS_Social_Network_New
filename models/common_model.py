from pydantic import BaseModel, field_validator


class ResultModel(BaseModel):
    data: dict
    messages: list
    fieldsErrors: list
    resultCode: int

    @field_validator('resultCode')
    def check_result_code(cls, value):
        if value != 0:
            raise ValueError('Result code should be 0')
        return value


class NegativeResultModel(BaseModel):
    data: dict
    messages: list[str]
    fieldsErrors: list
    resultCode: int

    @field_validator('resultCode')
    def check_result_code(cls, value):
        if not value:
            raise ValueError('Check result code value')
        return value


class NotAuthModel(BaseModel):
    message: str

    @field_validator('message')
    def check_error_message(cls, value):
        if value != 'Authorization has been denied for this request.':
            raise ValueError('Check error message for not auth user')
        return value



