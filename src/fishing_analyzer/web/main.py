from __future__ import annotations

from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fishing_analyzer.web.dashboard_service import (
    DashboardFilters,
    build_dashboard_data,
    list_fish_types,
    list_years,
)

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="Fishing Analyzer Dashboard", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def _normalize_fish_type(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


@app.get("/", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    year: int | None = None,
    fish_type: str | None = None,
) -> HTMLResponse:
    filters = DashboardFilters(year=year, fish_type=_normalize_fish_type(fish_type))
    dashboard = build_dashboard_data(filters)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "years": list_years(),
            "fish_types": list_fish_types(),
            "filters": filters,
            "dashboard": dashboard,
        },
    )


@app.get("/partials/dashboard", response_class=HTMLResponse)
async def dashboard_partial(
    request: Request,
    year: int | None = None,
    fish_type: str | None = None,
) -> HTMLResponse:
    filters = DashboardFilters(year=year, fish_type=_normalize_fish_type(fish_type))
    dashboard = build_dashboard_data(filters)

    return templates.TemplateResponse(
        request,
        "partials/dashboard_content.html",
        {
            "dashboard": dashboard,
        },
    )


def run() -> None:
    uvicorn.run(
        "fishing_analyzer.web.main:app",
        host="0.0.0.0",
        port=8085,
    )


if __name__ == "__main__":
    run()
