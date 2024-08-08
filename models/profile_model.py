from pydantic import BaseModel, field_validator, HttpUrl


class Contacts(BaseModel):
    facebook: HttpUrl | None
    website: HttpUrl | None
    vk: HttpUrl | None
    twitter: HttpUrl | None
    instagram: HttpUrl | None
    youtube: HttpUrl | None
    github: HttpUrl | None
    mainLink: HttpUrl | None


class Photos(BaseModel):
    small: HttpUrl | None
    large: HttpUrl | None


class ProfileModel(BaseModel):
    aboutMe: str
    contacts: Contacts
    lookingForAJob: bool
    lookingForAJobDescription: str
    fullName: str
    userId: int
    photos: Photos


class StatusModel(BaseModel):
    response: str


class Data(BaseModel):
    photos: Photos


class ProfilePhotosModel(BaseModel):
    data: Data
    messages: list
    fieldsErrors: list
    resultCode: int

