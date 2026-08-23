# Task API — FlyRank W2 A1

This is a small FastAPI task API that implements the mandatory W2 A1 CRUD
contract. It uses an in-memory list of exactly three starter tasks and exposes
validated list, read, create, partial update, and delete operations.

## Clean install and run

From the workspace root, install and start the server on the required local
port with one command:

```bash
pnpm install && PORT=8000 pnpm --filter @workspace/flyrank-backend-assignment-1 run dev
```

Then open:

- API: `http://localhost:8000`
- Interactive Swagger UI: `http://localhost:8000/docs`

## Assignment contract

### System responses

| Method | Path | Exact successful response |
| --- | --- | --- |
| `GET` | `/` | `{"name":"Task API","version":"1.0","endpoints":["/tasks"]}` |
| `GET` | `/health` | `{"status":"ok"}` |

### Task model

Every task has exactly these fields:

```json
{"id": 1, "title": "Plan the Task API", "done": false}
```

`id` is assigned by the API, `title` is required and cannot be blank, and
`done` defaults to `false` when a task is created. The server starts with
exactly three in-memory tasks.

### Endpoints and status codes

| Method | Path | Request body | Success | Error behavior |
| --- | --- | --- | --- | --- |
| `GET` | `/tasks` | — | `200` list of tasks | — |
| `GET` | `/tasks/{id}` | — | `200` task | `404` if absent |
| `POST` | `/tasks` | `{"title":"..."}` | `201` new task with next ID and `done:false` | `400` if title is missing, blank, or invalid |
| `PUT` | `/tasks/{id}` | `{"title":"..."}` and/or `{"done":true}` | `200` updated task | `400` for empty/invalid body; `404` if absent |
| `DELETE` | `/tasks/{id}` | — | `204` with no response body | `404` if absent |

All invalid request and not-found responses use the assignment error envelope:

```json
{"error":"Invalid request"}
```

or:

```json
{"error":"Task not found"}
```

`PUT` is partial: omitted fields retain their existing values. For example,
`{"done": true}` changes only the `done` value.

## Real curl verification

The following `curl -i` output was captured from the running server on
2026-08-23 during the verified CRUD cycle:

```text
HTTP/1.1 201 Created
date: Sun, 23 Aug 2026 09:37:40 GMT
server: uvicorn
content-length: 49
content-type: application/json

{"title":"Review submission","done":false,"id":4}
```

The full live sequence—including root, health, list, get, create, full update,
partial title update, partial done update, invalid requests, delete, and missing
task checks—is recorded in
[`VERIFICATION_EVIDENCE.md`](./VERIFICATION_EVIDENCE.md).

## Swagger UI

FastAPI generates Swagger UI from the same OpenAPI contract used by the tests.
Every system and CRUD operation has a visible summary and description. The
following screenshot was captured from the running API at `/docs` after the
live verification:

![Swagger UI showing the system and full task CRUD operations](./docs/swagger-ui.jpg)

Use Swagger UI's **Try it out** controls with the request bodies in the endpoint
table to exercise the same full CRUD cycle interactively.

## Testing

Run the automated contract suite:

```bash
pnpm --filter @workspace/flyrank-backend-assignment-1 test
```

The tests assert exact root/health responses, the `id`/`title`/`done` task
schema, starter tasks, CRUD status codes, required `error` envelopes, empty
`PUT` rejection, partial-field preservation, `204` empty bodies, and complete
Swagger/OpenAPI route descriptions.

## In-memory limitation

Tasks are stored only in a mutable Python list. All task changes reset whenever
the server restarts. This assignment intentionally does not add a database,
persistence layer, authentication, Docker, AI functionality, or optional
features.

## Submission evidence

- Public repository:
  [github.com/NiknaxTheGreek/flyrank-w2-a1-task-api](https://github.com/NiknaxTheGreek/flyrank-w2-a1-task-api)
- [`REQUIREMENTS_AUDIT.md`](./REQUIREMENTS_AUDIT.md) maps the mandatory W2 A1
  contract to implementation and verification.
- [`VERIFICATION_EVIDENCE.md`](./VERIFICATION_EVIDENCE.md) records the exact
  command outputs and live HTTP checks run for this submission.