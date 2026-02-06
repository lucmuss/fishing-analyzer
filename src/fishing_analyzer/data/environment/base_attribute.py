from __future__ import annotations

import os
from typing import Any

import pandas as pd

from fishing_analyzer import config


class BaseAttribute:
    """Basisklasse für Umweltattribute, die grundlegende Eigenschaften und Datenverarbeitung bereitstellt."""

    attribute_name: str | None
    file_location: str | None
    data_dict: dict[Any, Any]

    def __init__(self, file_location: str | None = None, attribute_name: str | None = None) -> None:
        self.attribute_name = attribute_name
        self.file_location = file_location
        self.data_dict = {}

    @property
    def series(self):
        data_values = list(self.data_dict.values())
        index_values = list(self.data_dict.keys())
        series = pd.Series(data_values, index=index_values, name=self.attribute_name)
        series = series.sort_index()

        mask = (series.index >= config.MINIMAL_BEGIN_DATE) & (
            series.index <= config.MAXIMAL_END_DATE
        )
        reduced_series = series.loc[mask]
        return reduced_series

    @property
    def abs_file_location(self):
        return_value = None

        if self.file_location:
            location_list = self.file_location.split("/")
            location_paths = location_list[:-1]
            location_file = location_list[len(location_list) - 1]

            script_dir = os.path.dirname(__file__)

            abs_file_path = os.path.join(script_dir, *location_paths)
            return_value = os.path.join(abs_file_path, location_file)

        return return_value

    def __repr__(self):
        return f"<{self.__class__.__name__} [{self.attribute_name}]>"
