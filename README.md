# usermanagementproject

Personalone FastAPI CRUD API for users, user profiles, categories, and tasks.

FastAPI CRUD API for users, user profiles, categories, and tasks. Resource code is grouped by layer under `app/routers`, `app/services`, `app/dao`, `app/models`, and `app/schemas`. Database connection and session setup live under `app/database`.

## Run

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Database settings are read from the root `.env` file. The default uses SQLite at `./personalone.db`; set `DATABASE_URL` to a PostgreSQL connection string and `DB_SCHEMA` to the schema name to use PostgreSQL. The configured PostgreSQL schema is created automatically. Open `http://127.0.0.1:8000/docs` for interactive API docs.

## CRUD routes

Each resource supports `POST /`, `GET /`, `GET /{id}`, `PATCH /{id}`, and `DELETE /{id}` under `/api/v1`:

- `/users`
- `/user-profiles`
- `/categories`
- `/tasks`

User passwords are stored as salted PBKDF2-SHA256 hashes and never included in API responses. This starter uses `create_all` on startup; use schema migrations for production changes.

`GET /api/v1/users/{user_id}/details` returns the user, their profile, categories, and tasks in one response.
