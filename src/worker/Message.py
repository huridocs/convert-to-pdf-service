from pydantic import BaseModel
from Params import Params


class Message(BaseModel):
    namespace: str
    task: str
    params: Params
    success: bool
    error_message: str | None = None
    file_url: str | None = None
