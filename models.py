from pydantic import BaseModel
from datetime import datetime


# это сделано для того, чтобы тело простых ответов (как правило, int либо str)
# складывать в модель без валидации
class Body(object):
    def __init__(self, value):
        self.value = value


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    requested_at: datetime = None


# модель простого ответа, которая складывает в body все, что придет.
# для ответов, у которых нет никакой вложенности
class SimpleResponse(BaseModel):
    status: bool
    body: Body

    class Config:
        arbitrary_types_allowed = True

