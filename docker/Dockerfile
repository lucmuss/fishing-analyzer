FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY assets ./assets
COPY docker/entrypoint.sh docker/entrypoint.sh

RUN chmod +x docker/entrypoint.sh
RUN uv sync --extra dev --frozen

EXPOSE 8085

HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD curl -fsS http://localhost:8085/ >/dev/null || exit 1

ENTRYPOINT ["bash", "docker/entrypoint.sh"]
