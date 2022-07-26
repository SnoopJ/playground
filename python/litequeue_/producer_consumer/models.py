from uuid import uuid4
from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    data: int


class CreateResponse(BaseModel):
    task_id: str
    queue_row: int


def _make_taskid():
    return str(uuid4())


class Task(BaseModel):
    request: CreateRequest
    task_id: str = Field(default_factory=_make_taskid)
