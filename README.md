# devflow-api

REST API for **DevFlow**, the open-source team task-management product. Part of
[OwlGuild](https://github.com/OwlGuild).

[![CI](https://github.com/OwlGuild/devflow-api/actions/workflows/ci.yml/badge.svg)](https://github.com/OwlGuild/devflow-api/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.2-092E20.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.18-brightgreen.svg)](https://www.django-rest-framework.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**Live:** https://devflow-api-jtmi.onrender.com/health/ · [readiness](https://devflow-api-jtmi.onrender.com/health/ready/)

## Why this exists

Task tools fail on two fronts: they are slow to respond, or they are a black box about what
your team is doing. This API keeps the data model small enough to reason about and the
endpoints boring on purpose, so the hard part stays the product logic rather than the plumbing.

## Quickstart

```bash
git clone https://github.com/OwlGuild/devflow-api.git
cd devflow-api
cp .env.example .env
docker compose -f docker-compose.dev.yml up --build
```

Local health check:

```bash
curl http://localhost:8000/health/
# {"status": "ok", "service": "devflow-api"}
```

## API

| Method | Path | Description |
|---|---|---|
| `GET` | `/health/` | liveness probe used by CI and uptime checks |
| `GET` | `/health/ready/` | readiness probe, verifies the database |

Endpoints are added behind the same contract: JSON in, JSON out, explicit status codes, and
a test for every behaviour change.

## Stack

| Layer | Choice |
|---|---|
| Runtime | Python 3.12 |
| Framework | Django 5 + Django REST Framework |
| Database | PostgreSQL 16, SQLite for tests |
| Server | Django dev server locally, Gunicorn in Docker |
| Container | Docker + docker-compose (api, Postgres) |

## Testing

```bash
pip install -r requirements.txt
pytest -q
# 8 passed
```

The suite covers contract behaviour — status codes, response shape and routing — rather than
implementation details, so refactors do not fail the build while a broken API would. CI runs
`manage.py check`, `check --deploy`, `pytest` and a Docker build on every push.

## Roadmap

- Task, project and membership models with migrations
- Authentication and workspace-scoped permissions
- Celery workers on Redis for background jobs
- OpenAPI schema published for `devflow-web` to generate types from

## Ownership

Both maintainers of [OwlGuild](https://github.com/OwlGuild) commit here.

| Area | Maintainer |
|---|---|
| Domain models, endpoints, migrations | [@MarziehAkrami](https://github.com/MarziehAkrami) |
| Client integration | [@AhmadGolbooee](https://github.com/AhmadGolbooee) |
| CI, Docker, docs | shared |

## License

[MIT](LICENSE).