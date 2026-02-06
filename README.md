# Fishing Analyzer

Fishing Analyzer now runs as a lightweight server-rendered dashboard with:
- FastAPI
- Jinja2 templates
- HTMX for partial updates
- Tailwind (CDN)

A legacy Dash implementation is still present under `src/fishing_analyzer/apps/`.

## Why this stack
- Python-first and minimal operational overhead
- No SPA build pipeline required
- Easy server-side rendering and progressive enhancement with HTMX
- Good fit for dashboard-only use cases without auth/admin complexity

## Repository Layout
- `src/fishing_analyzer/web/`: FastAPI app, templates, dashboard service
- `src/fishing_analyzer/data/`: fish dataset and legacy environment loaders
- `src/fishing_analyzer/apps/`: legacy Dash pages
- `docker/`: container Dockerfile and entrypoint
- `docs/`: development and release notes
- `tests/`: unit tests

## Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Setup
```bash
just setup
```

## Run (FastAPI dashboard)
```bash
just dev
```

Open: `http://localhost:8085`

## Legacy Dash mode
```bash
just dev-legacy
```

## Development Commands
```bash
just format
just lint
just typecheck
just test
just check
just ci
```

## Docker
```bash
just docker-up
just docker-down
```

By default Docker runs the FastAPI dashboard and does not require MongoDB.

## Optional Mongo Integration
If you want to run legacy Mongo-backed imports in container mode:
- set `RUN_WITH_MONGO=true`
- set `RUN_DATA_IMPORT=true`
- provide `MONGODB_URI`

## Release Workflow
- CI entry: `.github/workflows/ci.yml`
- Reusable jobs: lint, typecheck, tests, build, binary
- Release jobs: PyPI/TestPyPI + binaries

Tag-based release:
```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

## Troubleshooting
- `ModuleNotFoundError`: run `just setup` again.
- If template changes do not show: restart `just dev`.
- If lockfile drift happens: run `uv lock` and commit `uv.lock`.
