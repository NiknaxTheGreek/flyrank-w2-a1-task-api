# W2 A1 verification evidence

This evidence records commands and HTTP checks actually executed against the
corrected local Task API on 2026-08-23.

## Automated contract tests

Executed from the workspace root:

```bash
pnpm --filter @workspace/flyrank-backend-assignment-1 test
```

Observed result:

```text
21 passed, 1 warning in 0.43s
```

The warning was a Starlette deprecation warning about the installed HTTPX
integration. It did not fail the test run.

## Live curl cycle

The managed API workflow was restarted and served on
`http://127.0.0.1:8000`. The following cycle was executed at
`2026-08-23T09:37:41Z`.

| Request | Observed result |
| --- | --- |
| `GET /` | `200`; `{"name":"Task API","version":"1.0","endpoints":["/tasks"]}` |
| `GET /health` | `200`; `{"status":"ok"}` |
| `GET /tasks` | `200`; exactly the three starter tasks with `id`, `title`, and `done` fields |
| `GET /tasks/1` | `200`; returned task 1 |
| `GET /tasks/999` | `404`; `{"error":"Task not found"}` |
| `POST /tasks` with `{"title":"Review submission"}` | `201`; returned ID 4 with `done:false` |
| `POST /tasks` with `{}` | `400`; `{"error":"Invalid request"}` |
| Full `PUT /tasks/4` | `200`; title and done changed |
| Partial title `PUT /tasks/4` | `200`; `done:true` preserved |
| Partial done `PUT /tasks/4` | `200`; title preserved |
| Empty `PUT /tasks/4` body `{}` | `400`; `{"error":"Invalid request"}` |
| `PUT /tasks/999` | `404`; `{"error":"Task not found"}` |
| `DELETE /tasks/4` | `204`; response body size `0` bytes |
| `DELETE /tasks/999` | `404`; `{"error":"Task not found"}` |
| `GET /docs` | `200`; Swagger UI response body size `1007` bytes |
| `GET /openapi.json` | Seven operations; every operation had a non-empty summary and description |

### Actual `curl -i` output

```text
HTTP/1.1 201 Created
date: Sun, 23 Aug 2026 09:37:40 GMT
server: uvicorn
content-length: 49
content-type: application/json

{"title":"Review submission","done":false,"id":4}
```

### Swagger UI evidence

`docs/swagger-ui.jpg` is a screenshot captured from the running
`http://127.0.0.1:8000/docs` page after this verification. It shows the root,
health, and all five task CRUD operations with their visible summaries.