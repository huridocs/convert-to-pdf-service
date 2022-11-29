from pydantic import BaseModel
from Params import Params


class Task(BaseModel):
    task: str
    params: Params
