from __future__ import annotations

from calendar import month_name
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class DashboardFilters:
    year: int | None = None
    fish_type: str | None = None


@dataclass(frozen=True)
class DashboardData:
    total_catches: int
    unique_fish_types: int
    busiest_month: str
    busiest_month_count: int
    monthly_counts: list[tuple[str, int]]
    fish_type_counts: list[tuple[str, int]]
    recent_catches: list[dict[str, str]]


def _fish_csv_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "fish_database.csv"


@lru_cache(maxsize=1)
def load_catches_frame() -> pd.DataFrame:
    csv_path = _fish_csv_path()
    frame = pd.read_csv(
        csv_path,
        sep=";",
        header=None,
        names=["fish_type", "catch_date", "catch_time"],
        dtype=str,
    )

    frame["timestamp"] = pd.to_datetime(
        frame["catch_date"] + " " + frame["catch_time"],
        format="%d.%m.%Y %H:%M:%S",
        errors="coerce",
    )
    frame = frame.dropna(subset=["timestamp"]).copy()
    frame["fish_type"] = frame["fish_type"].astype(str).str.strip()
    frame = frame[frame["fish_type"] != ""].copy()

    frame["year"] = frame["timestamp"].dt.year
    frame["month"] = frame["timestamp"].dt.month
    frame["month_name"] = frame["month"].map(lambda value: month_name[int(value)])
    frame = frame.sort_values("timestamp")

    return frame


def list_years() -> list[int]:
    frame = load_catches_frame()
    return sorted(frame["year"].astype(int).unique().tolist())


def list_fish_types() -> list[str]:
    frame = load_catches_frame()
    return sorted(frame["fish_type"].dropna().unique().tolist())


def filter_frame(filters: DashboardFilters) -> pd.DataFrame:
    frame = load_catches_frame().copy()

    if filters.year is not None:
        frame = frame[frame["year"] == filters.year]

    if filters.fish_type:
        frame = frame[frame["fish_type"] == filters.fish_type]

    return frame


def build_dashboard_data(filters: DashboardFilters) -> DashboardData:
    frame = filter_frame(filters)

    if frame.empty:
        return DashboardData(
            total_catches=0,
            unique_fish_types=0,
            busiest_month="-",
            busiest_month_count=0,
            monthly_counts=[],
            fish_type_counts=[],
            recent_catches=[],
        )

    monthly_series = frame.groupby("month").size().sort_index()
    fish_series = frame.groupby("fish_type").size().sort_values(ascending=False)

    busiest_month_number = int(monthly_series.idxmax())
    busiest_month = month_name[busiest_month_number]
    busiest_month_count = int(monthly_series.max())

    monthly_counts = [
        (month_name[int(month_number)], int(count))
        for month_number, count in monthly_series.items()
    ]
    fish_type_counts = [(fish, int(count)) for fish, count in fish_series.items()]

    recent = frame.tail(12)
    recent_catches = [
        {
            "fish_type": str(row.fish_type),
            "datetime": row.timestamp.strftime("%Y-%m-%d %H:%M"),
        }
        for row in recent.itertuples(index=False)
    ]

    return DashboardData(
        total_catches=int(len(frame)),
        unique_fish_types=int(frame["fish_type"].nunique()),
        busiest_month=busiest_month,
        busiest_month_count=busiest_month_count,
        monthly_counts=monthly_counts,
        fish_type_counts=fish_type_counts,
        recent_catches=recent_catches,
    )
