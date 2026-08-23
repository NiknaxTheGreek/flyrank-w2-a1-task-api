# W2 A1 mandatory requirements audit

This audit covers only the required W2 A1 task API work. AI Rematch and all
optional/stretch work are explicitly excluded.

| Mandatory requirement | Status | Implementation and verification |
| --- | --- | --- |
| Server is available on `localhost:8000` | Complete | Artifact service port and `PORT` are both 8000; live curl checks used `http://127.0.0.1:8000`. |
| `GET /` exact response | Complete | `app/main.py` returns `{"name":"Task API","version":"1.0","endpoints":["/tasks"]}`; automated and live checks pass. |
| `GET /health` exact response | Complete | `app/main.py` returns `{"status":"ok"}`; automated and live checks pass. |
| Exactly three in-memory starter tasks | Complete | `app/storage.py` contains three `id`/`title`/`done` tasks; automated and live list checks pass. |
| List/get task routes | Complete | `GET /tasks` and `GET /tasks/{task_id}` are implemented and tested. |
| Missing task errors | Complete | Missing IDs return `404` with `{"error":"Task not found"}`. |
| Create task behavior | Complete | `POST /tasks` assigns the next ID, defaults `done` to false, and returns `201`. |
| Invalid create behavior | Complete | Missing, empty, null, and unknown input return `400` with an `error` key. |
| Partial update behavior | Complete | `PUT` accepts title and/or done, preserves omitted fields, and returns `200`. |
| Empty/invalid update behavior | Complete | Empty, null, invalid-type, and unknown-field payloads return `400` with an `error` key. |
| Update/delete missing task behavior | Complete | Both return `404` with an `error` key. |
| Delete response | Complete | Successful deletion returns `204` with an empty body. |
| Swagger endpoint summaries/descriptions | Complete | Explicit route metadata is implemented; automated OpenAPI test and live OpenAPI inspection confirm all seven operations are described. |
| Curl and Swagger evidence | Complete | `VERIFICATION_EVIDENCE.md` records the live curl cycle; `docs/swagger-ui.jpg` is a genuine capture of the live Swagger UI. |
| README submission documentation | Complete | README includes purpose, one-command run path, endpoint table, real `curl -i` output, Swagger screenshot, test command, and in-memory limitation. |
| No prohibited extras | Complete | No database, persistence, auth, Docker, AI, AI Rematch, or optional features were added. |

## Public repository and honest commit history

The verified submission snapshot is public at
[github.com/NiknaxTheGreek/flyrank-w2-a1-task-api](https://github.com/NiknaxTheGreek/flyrank-w2-a1-task-api).

The local `main` branch contains the honest implementation history, including
the port-8000 runtime change, the exact W2 A1 API/test change, and the
documentation/evidence change. The public repository was populated through the
authenticated GitHub API because direct Git transport could not use the
connector-managed OAuth credential.