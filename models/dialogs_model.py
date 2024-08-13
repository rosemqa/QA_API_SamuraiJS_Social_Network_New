from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class Photos(BaseModel):
    small: HttpUrl | None
    large: HttpUrl | None


class DialogsListItem(BaseModel):
    id: int
    userName: str
    hasNewMessages: bool
    lastDialogActivityDate: datetime
    lastUserActivityDate: datetime
    newMessagesCount: int
    photos: Photos


class AllDialogsModel(BaseModel):
    response: list[DialogsListItem]


class GetMessage(BaseModel):
    id: UUID
    body: str
    translatedBody: None
    addedAt: datetime
    senderId: int
    senderName: str
    recipientId: int
    viewed: bool


class MessageListModel(BaseModel):
    items: list[GetMessage]


class PostMessageDetails(BaseModel):
    id: UUID
    body: str
    translatedBody: None
    addedAt: datetime
    senderId: int
    senderName: str
    recipientId: int
    viewed: bool
    deletedBySender: bool
    deletedByRecipient: bool
    isSpam: bool
    distributionId: None


class PostMessage(BaseModel):
    message: PostMessageDetails


class SendMessageModel(BaseModel):
    data: PostMessage
    messages: list
    fieldsErrors: list
    resultCode: int


class IsMessageViewedModel(BaseModel):
    response: bool


class NewMessagesCountModel(BaseModel):
    response: int
