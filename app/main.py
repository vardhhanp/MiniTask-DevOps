from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="MiniTask DevOps Assessment",
    version="1.0.0"
)

TASKS: list[dict] = []


# Request Model
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=80)


# Health Check
@app.get("/health")
def health():
    return {"status": "ok"}


# Get All Tasks
@app.get("/tasks")
def list_tasks():
    return {"tasks": TASKS}


# Create Task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    new_id = max(
        (t["id"] for t in TASKS),
        default=0
    ) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    TASKS.append(new_task)

    return new_task


# Update Task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):

    for t in TASKS:

        if t["id"] == task_id:

            t["title"] = task.title

            return t

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# Delete Task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for t in TASKS:

        if t["id"] == task_id:

            TASKS.remove(t)

            return {
                "message": "Task deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )