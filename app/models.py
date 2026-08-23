"""Pydantic models for the W2 A1 in-memory task API."""

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TaskBase(BaseModel):
    """Fields accepted when creating a task."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class TaskCreate(TaskBase):
    """Payload shape for creating a task."""


class TaskUpdate(BaseModel):
    """Payload shape for partially updating an existing task."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=200)
    done: bool | None = None

    @model_validator(mode="after")
    def update_must_contain_a_non_null_field(self) -> "TaskUpdate":
        """Reject empty payloads and explicit null values."""
        updates = self.model_dump(exclude_unset=True)
        if not updates:
            raise ValueError("Provide at least one field to update.")
        if any(value is None for value in updates.values()):
            raise ValueError("Update fields cannot be null.")
        return self


class Task(TaskBase):
    """A stored task with a positive integer identifier."""

    id: int = Field(gt=0)