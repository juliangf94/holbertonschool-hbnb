# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Layout

```
holbertonschool-hbnb/
├── part1-design/       UML diagrams and sequence diagrams (no code)
├── part2-backend-v1/   REST API with in-memory storage, no auth
├── part3-backend/      REST API with SQLAlchemy + JWT (main backend)
├── part4-frontend/     Vanilla JS frontend consuming Part 3 API
├── docs/               Personal notes (develop branch only)
└── Images/             Screenshots for README
```

---

## Running the Project

### Part 3 — Backend

```bash
cd part3-backend
source venv/bin/activate        # or: source .venv/bin/activate
cp .env.example .env            # set SECRET_KEY and JWT_SECRET_KEY
python3 run.py
```

- API: `http://127.0.0.1:5000/api/v1/`
- Swagger UI: `http://127.0.0.1:5000/api/v1/`
- DB auto-created at `instance/development.db` on first run
- Default admin: `admin@hbnb.io` / `admin1234`

### Part 4 — Frontend (requires Part 3 running)

```bash
cd part4-frontend
python3 -m http.server 8080
# Open http://localhost:8080
```

### Part 2 — In-memory backend (no auth, no DB)

```bash
cd part2-backend-v1
pip install -r requirements.txt
python3 run.py
```

---

## Tests (Part 3)

```bash
cd part3-backend
source venv/bin/activate
python3 -m pytest app/tests/ -v                          # all 120 tests
python3 -m pytest app/tests/test_part3.py -v             # 61 integration tests
python3 -m pytest app/tests/test_models.py -v            # 59 unit tests
python3 -m pytest app/tests/test_part3.py::TestAuth -v   # single class
```

`TestingConfig` uses `sqlite:///:memory:` — no file created, no cleanup needed.

---

## Architecture (Part 3)

### 3-Layer Facade Pattern

```
API layer        app/api/v1/*.py          Flask-RESTX namespaces
      ↓
Service layer    app/services/facade.py   HBnBFacade — single entry point
      ↓
Data layer       app/persistence/         SQLAlchemyRepository / UserRepository
```

**Rule:** API endpoints call only `HBnBFacade` methods. Never import models or repositories directly in API files.

### Key files

| File | Role |
|---|---|
| `app/__init__.py` | `create_app()` factory — registers all extensions and namespaces, calls `db.create_all()` |
| `app/extensions.py` | Shared `db`, `bcrypt`, `jwt` instances — import from here to avoid circular imports |
| `app/services/facade.py` | `HBnBFacade` — all business logic lives here |
| `app/persistence/repository.py` | `Repository` ABC + `InMemoryRepository` + `SQLAlchemyRepository` |
| `app/persistence/user_repository.py` | Extends `SQLAlchemyRepository` with `get_user_by_email()` |
| `app/models/base_model.py` | `BaseModel(db.Model)` with `__abstract__ = True` — provides `id` (UUID), `created_at`, `updated_at` |
| `config.py` | `DevelopmentConfig` / `TestingConfig` / `ProductionConfig` |

### Model relationships

- `Place` → `Review`: one-to-many (`backref='place'`)
- `Place` ↔ `Amenity`: many-to-many via `place_amenity` association table in `place.py`
- `Place` → `PlaceImage`: one-to-many with cascade delete
- `Review`, `Place` → `User`: many-to-one via FK

### JWT pattern

Login sets `identity=user.id` and `additional_claims={'is_admin': user.is_admin}`. Protected endpoints retrieve these with `get_jwt_identity()` and `get_jwt()`. Never query the DB to check admin status mid-request — read from the token claims.

---

## Config and Environment

`config.py` defines three configs selected by passing the class to `create_app()`:

| Config | DB | Use |
|---|---|---|
| `DevelopmentConfig` | `instance/development.db` (SQLite file) | Default / `python3 run.py` |
| `TestingConfig` | `sqlite:///:memory:` | pytest |
| `ProductionConfig` | `DATABASE_URL` env var | MySQL |

`.env` must define `SECRET_KEY` and `JWT_SECRET_KEY`. The file is gitignored; copy from `.env.example`.

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, public-facing code |
| `develop` | Active development — merge here first |
| `testing` | QA before merging to main |

Personal notes (`docs/`) exist only on `develop`, not on `main`.

---

## Frontend (Part 4)

All pages load `JS/common.js` first for shared utilities (`getCookie`, `setCookie`, `checkAuthentication`, `API_URL`). Each page then loads its own JS module. No bundler — plain `<script>` tags.

`API_URL` is hardcoded to `http://127.0.0.1:5000/api/v1` in `JS/common.js`. Change this if the backend runs on a different port.

JWT is stored in a cookie named `token` (1-day expiry, `SameSite=Lax`). Auth state is checked on every page load via `checkAuthentication()`.
