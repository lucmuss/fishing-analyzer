import pytest

from fishing_analyzer import config


@pytest.mark.unit
def test_get_year_range_inclusive() -> None:
    years = config.get_year_range("2013-01-01 00:00:00", "2015-12-31 00:00:00")
    assert years == ["2013", "2014", "2015"]


@pytest.mark.unit
def test_month_name_dictionary_shape() -> None:
    month_dict = config.get_month_name_dict()
    assert len(month_dict) == 12
    assert month_dict["1"] == "January"
    assert month_dict["12"] == "December"


@pytest.mark.unit
def test_month_days_dictionary_shape() -> None:
    month_days = config.get_month_days_dict()
    assert len(month_days) == 12
    assert set(month_days.keys()) == set(range(1, 13))
