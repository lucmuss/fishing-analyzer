# Fishing Analyzer

Fishing Analyzer is a Dash application for exploring fish catch records together with
weather and water-related attributes.

## Features
- Interactive Dash UI with pages for statistics, histograms, distributions, and data entry.
- MongoDB-backed fish record storage.
- Import tooling for fish CSV and environment raw datasets.
- Reproducible local workflow with `uv`, `Justfile`, and pre-commit hooks.
- Modular GitHub Actions workflows for lint, typecheck, tests, build, binary, and release.

## Repository Layout
- `src/fishing_analyzer/`: application source code.
- `assets/`: static frontend assets used by Dash.
- `docker/`: container Dockerfile and entrypoint.
- `docs/`: development and release documentation.
- `examples/`: small usage examples.
- `.github/workflows/`: CI and release pipelines.

## Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- MongoDB (local or remote)
- Docker (optional)

## Installation
```bash
just setup
```

Manual equivalent:
```bash
uv venv
UV_PROJECT_ENVIRONMENT=.venv uv sync --extra dev
cp -n .env.example .env
```

## Configuration
Copy `.env.example` to `.env` and adjust values:
- `SECRET_KEY`: Flask secret key.
- `MONGODB_URI`: MongoDB connection string.
- `RUN_AS_PRODUCTION`: set `true` for non-debug server mode.
- `RUN_TESTS`: optional container startup test execution.
- `RUN_DATA_IMPORT`: optional startup data import.

## Usage
Run the app locally:
```bash
just dev
```

Or directly:
```bash
uv run python -m fishing_analyzer.run
```

Import source data into MongoDB:
```bash
uv run python -m fishing_analyzer.tools.import_db
```

Run complete bootstrap (import + diagram generation):
```bash
uv run python -m fishing_analyzer.install
```

## Examples
```bash
uv run python examples/basic_usage.py
```

## Development Workflow
Main commands:
```bash
just format
just lint
just typecheck
just test
just check
just ci
```

Pre-commit:
```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Docker Workflow
Build and start:
```bash
just docker-up
```

Stop:
```bash
just docker-down
```

Default app port: `8085`.

## CI/CD and Release
- Main CI entry: `.github/workflows/ci.yml`
- Reusable workflows:
  - `ci-lint.yml`
  - `ci-typecheck.yml`
  - `ci-tests.yml`
  - `ci-build.yml`
  - `ci-binary.yml`
- Release workflows:
  - `publish-to-pypi.yml`
  - `build-binaries.yml`

Release steps:
1. Run `just ci`.
2. Tag a release: `git tag vX.Y.Z && git push origin vX.Y.Z`.
3. Tag push publishes package and triggers binary build/release assets.
4. For TestPyPI, trigger `publish-to-pypi.yml` manually with `target=testpypi`.

## Troubleshooting
- `ModuleNotFoundError: fishing_analyzer`: run `just setup` again.
- Mongo connection errors: verify `MONGODB_URI` and Mongo health.
- CI lock mismatch: refresh lock with `uv lock` and commit `uv.lock`.
- Dash page errors after import changes: clear generated caches with `just clean`.
