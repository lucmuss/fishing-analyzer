set shell := ["bash", "-euo", "pipefail", "-c"]
set dotenv-load := true

default:
    @just --list

setup:
    uv venv
    UV_PROJECT_ENVIRONMENT=.venv uv sync --extra dev
    cp -n .env.example .env || true

dev:
    uv run uvicorn fishing_analyzer.web.main:app --host 0.0.0.0 --port 8085 --reload

dev-legacy:
    uv run python -m fishing_analyzer.run

format:
    uv run ruff format src tests
    uv run ruff check --fix src tests

lint:
    uv run ruff check src tests
    uv run ruff format --check src tests
    uv run --with black black --check src tests
    uv run --with flake8 flake8 src tests

typecheck:
    uv run mypy src tests

test:
    uv run pytest

check: lint typecheck test

build:
    rm -rf dist build
    uv run --with build python -m build
    uv run --with twine twine check dist/*

binary:
    rm -rf dist build
    uv run --with pyinstaller pyinstaller --onefile --name fishing-analyzer src/fishing_analyzer/run.py

ci: check build

docker-up:
    docker compose up -d --build
    docker compose logs -f app

docker-down:
    docker compose down --remove-orphans

clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    rm -rf .pytest_cache .coverage htmlcov .ruff_cache .mypy_cache build dist .pyinstaller
