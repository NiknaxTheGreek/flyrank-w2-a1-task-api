"""Tests for the exact FlyRank W2 A1 CRUD API contract."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import Task
from app.storage import tasks


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tasks() -> None:
    """Keep CRUD tests independent while using the real in-memory store."""
    original_tasks = [task.model_copy(deep=True) for task in tasks]
    tasks[:] = [
        Task(
            id=1,
            title="Plan the Task API",
            done=False,
        ),
        Task(
            id=2,
            title="Write CRUD routes",
            done=False,
        ),
        Task(
            id=3,
            title="Verify the API",
            done=True,
        ),
    ]
    yield
    tasks[:] = original_tasks


def assert_error(response, status_code: int) -> None:
    """Assert the required error status and JSON envelope."""
    assert response.status_code == status_code
    assert list(response.json()) == ["error"]
    assert isinstance(response.json()["error"], str)


def test_root_returns_the_exact_assignment_response() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


def test_health_returns_the_exact_assignment_response() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_tasks_returns_three_in_memory_tasks() -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Plan the Task API", "done": False},
        {"id": 2, "title": "Write CRUD routes", "done": False},
        {"id": 3, "title": "Verify the API", "done": True},
    ]


def test_get_task_returns_requested_task() -> None:
    response = client.get("/tasks/2")

    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "title": "Write CRUD routes",
        "done": False,
    }


def test_get_missing_task_uses_the_error_envelope() -> None:
    assert_error(client.get("/tasks/999"), 404)


def test_create_task_assigns_the_next_id_and_default_done_value() -> None:
    response = client.post("/tasks", json={"title": "Created task"})

    assert response.status_code == 201
    assert response.json() == {
        "id": 4,
        "title": "Created task",
        "done": False,
    }


@pytest.mark.parametrize("payload", [{}, {"title": "   "}, {"title": None}])
def test_create_rejects_missing_or_empty_title(payload: dict) -> None:
    assert_error(client.post("/tasks", json=payload), 400)


def test_create_rejects_unknown_fields_with_the_error_envelope() -> None:
    assert_error(client.post("/tasks", json={"title": "Wrong", "completed": False}), 400)


def test_full_update_returns_the_exact_updated_task() -> None:
    response = client.put(
        "/tasks/1",
        json={
            "title": "Fully updated task",
            "done": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Fully updated task",
        "done": True,
    }


def test_partial_done_update_preserves_title() -> None:
    response = client.put("/tasks/1", json={"done": True})

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Plan the Task API",
        "done": True,
    }


def test_partial_title_update_preserves_done() -> None:
    tasks[0] = tasks[0].model_copy(update={"done": True})

    response = client.put("/tasks/1", json={"title": "Updated title"})

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Updated title",
        "done": True,
    }


@pytest.mark.parametrize(
    "payload",
    [{}, {"done": None}, {"done": "not-a-boolean"}, {"completed": True}],
)
def test_update_rejects_empty_or_invalid_payloads(payload: dict) -> None:
    assert_error(client.put("/tasks/1", json=payload), 400)


def test_update_missing_task_uses_the_error_envelope() -> None:
    assert_error(client.put("/tasks/999", json={"done": True}), 404)


def test_delete_returns_204_with_empty_body() -> None:
    response = client.delete("/tasks/3")

    assert response.status_code == 204
    assert response.content == b""
    assert_error(client.get("/tasks/3"), 404)


def test_delete_missing_task_uses_the_error_envelope() -> None:
    assert_error(client.delete("/tasks/999"), 404)


def test_docs_and_openapi_describe_every_assignment_endpoint() -> None:
    response = client.get("/docs")

    assert response.status_code == 200
    assert "swagger-ui" in response.text

    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    paths = openapi.json()["paths"]
    expected_operations = {
        ("/", "get"),
        ("/health", "get"),
        ("/tasks", "get"),
        ("/tasks", "post"),
        ("/tasks/{task_id}", "get"),
        ("/tasks/{task_id}", "put"),
        ("/tasks/{task_id}", "delete"),
    }
    actual_operations = {
        (path, method)
        for path, methods in paths.items()
        for method in methods
    }
    assert expected_operations <= actual_operations
    for path, method in expected_operations:
        operation = paths[path][method]
        assert operation["summary"]
        assert operation["description"]