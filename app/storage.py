"""Temporary in-memory storage for the assignment."""

from .models import Task


tasks: list[Task] = [
    Task(
        id=1,
        title="Plan the Task API",
    ),
    Task(
        id=2,
        title="Write CRUD routes",
    ),
    Task(
        id=3,
        title="Verify the API",
        done=True,
    ),
]