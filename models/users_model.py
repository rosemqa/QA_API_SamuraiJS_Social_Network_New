from pydantic import BaseModel, field_validator, HttpUrl, AnyUrl


class Photos(BaseModel):
    small: HttpUrl | None
    large: HttpUrl | None

    @field_validator('small', 'large')
    def field_are_not_empty(cls, value):
        if value == "":
            raise ValueError('Field is empty')
        else:
            return value


class UserModel(BaseModel):
    name: str
    id: int
    uniqueUrlName: str | None
    photos: Photos
    status: str | None
    followed: bool

    @field_validator('name')
    def field_name_is_not_empty(cls, value):
        if not value:
            raise ValueError('Field "name" is empty')
        else:
            return value


class UserListPositiveModel(BaseModel):
    items: list[UserModel]
    totalCount: int
    error: None


class UserListNegativeModel(BaseModel):
    items: None
    totalCount: int
    error: str
