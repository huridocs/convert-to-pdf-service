from pydantic import BaseModel


class Params(BaseModel):
    filename: str
    namespace: str


class Task(BaseModel):
    task: str
    params: Params


class Message(BaseModel):
    namespace: str
    task: str
    params: Params
    success: bool
    error_message: str | None = None
    file_url: str | None = None
