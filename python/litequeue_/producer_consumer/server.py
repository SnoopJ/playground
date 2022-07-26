from fastapi import FastAPI
from litequeue import SQLQueue

from models import CreateResponse, CreateRequest, Task


app = FastAPI()

QUEUE = SQLQueue("tasks.sqlite")


@app.post("/submit", response_model=CreateResponse)
async def submit(request: CreateRequest):
    task = Task(request=request)
    queue_row = QUEUE.put(task.json())
    return CreateResponse(task_id=task.task_id, queue_row=queue_row)
