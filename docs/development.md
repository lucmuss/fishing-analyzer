# Development Workflow

## Prerequisites
- Python 3.11 or newer
- uv
- Docker (optional)

## Local Setup
```bash
just setup
```

## Daily Commands
```bash
just format
just check
just ci
```

## Pre-Commit
```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Test Strategy
- Unit tests cover pure helper logic.
- Integration tests should be added for MongoDB-backed flows.
- Keep slow tests behind the `slow` marker.
