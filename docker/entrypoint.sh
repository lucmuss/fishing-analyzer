#!/usr/bin/env bash
set -euo pipefail

wait_for_mongo() {
  local retries=30
  local delay=2

  echo "Waiting for MongoDB (${MONGODB_URI:-mongodb://localhost:27017})..."
  for _ in $(seq 1 "$retries"); do
    if uv run python - <<'PY'
from pymongo import MongoClient
from fishing_analyzer import config

client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=1000)
client.admin.command("ping")
print("MongoDB is reachable")
PY
    then
      return 0
    fi
    sleep "$delay"
  done

  echo "MongoDB is not reachable after retries." >&2
  return 1
}

wait_for_mongo

if [ "${RUN_TESTS:-false}" = "true" ]; then
  echo "Running test suite before app startup..."
  uv run pytest tests -m "not slow" --tb=short
fi

if [ "${RUN_DATA_IMPORT:-true}" = "true" ]; then
  echo "Running data import..."
  uv run python -m fishing_analyzer.tools.import_db
fi

echo "Starting Fishing Analyzer on port 8085..."
exec uv run python -m fishing_analyzer.run
