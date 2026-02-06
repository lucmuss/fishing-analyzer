import numpy as np
import pandas as pd
import pytest

from fishing_analyzer import config, utils


@pytest.mark.unit
def test_clean_series_replaces_nan_and_infinity() -> None:
    series = pd.Series([1.0, np.nan, np.inf, -np.inf])
    cleaned = utils.clean_series(series)
    assert cleaned.tolist() == [1.0, 0.0, 0.0, 0.0]


@pytest.mark.unit
def test_get_database_document_uses_template() -> None:
    document = utils.get_database_document("Aal", "2026-01-01 01:00:00", "fisher", "river")
    assert document == {
        "fish_type": "Aal",
        "catch_date": "2026-01-01 01:00:00",
        "fisher_id": "fisher",
        "river_id": "river",
    }


@pytest.mark.unit
def test_get_graph_name_formats_value() -> None:
    assert utils.get_graph_name("water_temperature", "Aal") == "Aal - Water Temperature"


@pytest.mark.unit
def test_has_correct_year_range() -> None:
    valid = f"{config.MINIMAL_YEAR_RANGE_INT}010100"
    invalid = f"{config.MINIMAL_YEAR_RANGE_INT - 1}123123"
    assert utils.has_correct_year_range(valid)
    assert not utils.has_correct_year_range(invalid)
