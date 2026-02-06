from calendar import month_name

from fishing_analyzer.web.dashboard_service import (
    DashboardFilters,
    build_dashboard_data,
    filter_frame,
    list_fish_types,
    list_years,
    load_catches_frame,
)


def test_load_catches_frame_has_expected_columns() -> None:
    frame = load_catches_frame()

    assert not frame.empty
    assert {"fish_type", "timestamp", "year", "month_name"}.issubset(frame.columns)


def test_filter_frame_by_year_restricts_results() -> None:
    years = list_years()
    selected_year = years[-1]

    filtered = filter_frame(DashboardFilters(year=selected_year))

    assert not filtered.empty
    assert set(filtered["year"].unique().tolist()) == {selected_year}


def test_build_dashboard_data_handles_empty_filter() -> None:
    fish_types = list_fish_types()
    impossible_fish = "__not_existing__"
    assert impossible_fish not in fish_types

    data = build_dashboard_data(DashboardFilters(year=1900, fish_type=impossible_fish))

    assert data.total_catches == 0
    assert data.unique_fish_types == 0
    assert data.monthly_counts == []
    assert data.fish_type_counts == []


def test_build_dashboard_data_months_are_sorted_chronologically() -> None:
    data = build_dashboard_data(DashboardFilters())
    month_to_index = {name: index for index, name in enumerate(month_name) if name}

    indices = [month_to_index[month] for month, _ in data.monthly_counts]

    assert indices == sorted(indices)
    assert data.busiest_month_count == max(count for _, count in data.monthly_counts)
