# Fishing Analyzer

This is a small example project where all caught fishes are tracked in the river Baunach.

## Technologies
The project uses MongoDB, Pandas, Plotly, Dash, and NumPy.

## Prerequisites
Install [Python Interpreter](https://www.python.org/) (Python 3.8+).

Install [uv](https://github.com/astral-sh/uv) package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup
```bash
# Install dependencies and setup environment
just setup

# For development with dev dependencies
uv sync --extra dev
```

## Database Prerequisites
Install [MongoDB](https://www.mongodb.com) on your computer.

Configuration is in `config.py`.

## Data Import
Run data import:
```bash
python install.py
```

## Running the App
```bash
# Development mode
just dev

# Or directly
python run.py
```

## Development Commands
```bash
# Format code
just format

# Lint code
just lint

# Run tests
just test

# Full check (lint + typecheck + test)
just check

# Clean artifacts
just clean
```

## Docker
```bash
# Build and run
just docker-up

# Stop
just docker-down
```

## Authors
* Data points - [Angel Verein Ebern](http://www.av-ebern.de/)
* Data points - [Angel Verein Baunach](http://www.anglerverein-baunach.de/)

