# DSA Forge

Personalized DSA practice platform. It uses FastAPI, SQLAlchemy, and a React/Vite client. SQLite remains the default for a single-machine setup; PostgreSQL can be configured for a shared database.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --port 8000

cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The API is available at `http://localhost:8000/docs`.

## Docker startup

Docker Desktop must be running. From the repository root:

```powershell
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="use-a-strong-local-password"
docker compose up --build
```

Open `http://localhost:5173`; the API is available at `http://localhost:8000/docs`. The API container uses the Docker socket only to launch short-lived, network-disabled executor containers. The executor image is built locally as `dsa-forge-executor:local` and is never exposed as a network service.

## Shared PostgreSQL database

To have multiple local installations use the same data, point each installation's API at the same PostgreSQL database. The database must be hosted somewhere all users' computers can reach (for example, a managed PostgreSQL service); a database running on one person's `localhost` is only reachable from that computer.

1. Copy `.env.example` to `.env` and replace `DATABASE_URL` with the connection URL from your PostgreSQL provider. Use the `postgresql+psycopg://` scheme. URL-encode special characters in the username or password. Keep `.env` private and out of source control.
2. Each user clones the project, creates their own `.env` with that same database URL, and starts the app normally. With Docker Compose, the API reads `DATABASE_URL` from `.env`; without Docker, export that variable before starting Uvicorn.
3. In the database provider's access settings, allow connections from each user's network and require TLS. Use a dedicated application database user with only the permissions the app needs, and rotate the password if it is shared beyond the team.

The API creates missing tables on startup. The default SQLite URL is retained when `DATABASE_URL` is not set. Do not put a live database password in this repository or send it in chat.
## Execution security

`POST /api/run` and `POST /api/submit` use a short-lived Docker container when Docker is installed. The supplied executor disables networking, drops capabilities, runs as an unprivileged user, has read-only root storage, and applies CPU/memory/process/output/time limits. Docker is not installed in this environment, so the API reports `503` instead of falling back to unsafe in-process execution.

For public use, put the executor on isolated hosts/VMs and add queueing, per-user rate limits, image scanning, kernel hardening, observability, and a stronger sandbox such as gVisor or Firecracker.

## Data and import format

With the default SQLite setup, the database is stored at `backend/dsa_forge.db`. PostgreSQL is selected by setting `DATABASE_URL`. Seed data is created automatically on first start. `GET /api/export` returns versioned JSON; `POST /api/import` accepts `{ "version": 1, "questions": [...] }` and validates required fields.

## Test

```powershell
pytest backend/tests
cd frontend; npm run build
```
