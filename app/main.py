"""FastAPI implementation for the FlyRank W2 A1 task API."""

from typing import Literal

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .models import Task, TaskCreate, TaskUpdate
from .storage import tasks


class RootResponse(BaseModel):
    """Exact response body required by the W2 A1 brief."""

    name: Literal["Task API"]
    version: Literal["1.0"]
    endpoints: list[Literal["/tasks"]]


class HealthResponse(BaseModel):
    """Exact health response required by the W2 A1 brief."""

    status: Literal["ok"]


app = FastAPI(
    title="Task API",
    version="1.0",
    description="An in-memory CRUD task API for the FlyRank W2 A1 assignment.",
)
app.state.tasks = tasks


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    _request: Request,
    _exc: RequestValidationError,
) -> JSONResponse:
    """Return the assignment-required JSON envelope for invalid requests."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid request"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    _request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """Return the assignment-required JSON envelope for HTTP failures."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc.detail)},
    )


@app.get(
    "/",
    response_model=RootResponse,
    tags=["system"],
    summary="Describe the task API",
    description="Return the exact assignment metadata for the Task API.",
)
async def root() -> RootResponse:
    """Return the exact task API metadata."""
    return RootResponse(name="Task API", version="1.0", endpoints=["/tasks"])


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["system"],
    summary="Check API health",
    description="Return the exact health response required by the assignment.",
)
async def health_check() -> HealthResponse:
    """Return a healthy status."""
    return HealthResponse(status="ok")


@app.get(
    "/tasks",
    response_model=list[Task],
    tags=["tasks"],
    summary="List tasks",
    description="Return all tasks held in the in-memory task list.",
)
async def list_tasks() -> list[Task]:
    """Return all tasks currently held in memory."""
    return tasks


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["tasks"],
    summary="Get a task",
    description="Return one in-memory task by its numeric identifier.",
)
async def get_task(task_id: int) -> Task:
    """Return one task by its identifier."""
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
    summary="Create a task",
    description="Create a task with the next integer ID and a default done value of false.",
)
async def create_task(task_input: TaskCreate) -> Task:
    """Create a task and assign the next available identifier."""
    next_id = max((task.id for task in tasks), default=0) + 1
    task = Task(id=next_id, **task_input.model_dump())
    tasks.append(task)
    return task


@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    tags=["tasks"],
    summary="Partially update a task",
    description="Update one or both of title and done while preserving omitted fields.",
)
async def update_task(task_id: int, task_input: TaskUpdate) -> Task:
    """Update only the fields supplied by the client."""
    task_index = next(
        (index for index, task in enumerate(tasks) if task.id == task_id),
        None,
    )
    if task_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    updated_task = tasks[task_index].model_copy(
        update=task_input.model_dump(exclude_unset=True)
    )
    tasks[task_index] = updated_task
    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
    summary="Delete a task",
    description="Remove one in-memory task and return an empty 204 response.",
)
async def delete_task(task_id: int) -> Response:
    """Delete a task from temporary in-memory storage."""
    task_index = next(
        (index for index, task in enumerate(tasks) if task.id == task_id),
        None,
    )
    if task_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    tasks.pop(task_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)