from pydantic import BaseModel


class IsFollowModel(BaseModel):
    response: bool
