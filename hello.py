from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Task Manager")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool = False


tasks: dict[int, Task] = {}
next_id: int = 1


@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/tasks", response_model=Task)
def create_task(payload: TaskCreate):
    global next_id
    task = Task(
        id=next_id,
        title=payload.title,
        description=payload.description,
        done=False,
    )
    tasks[task.id] = task
    next_id += 1
    return task