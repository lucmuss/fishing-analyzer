import datetime
from typing import Any

from fishing_analyzer import config
from fishing_analyzer.data.environment.base_attribute import BaseAttribute


class FishType(BaseAttribute):
    """Repräsentiert den Fischtyp pro Fang, abgeleitet von BaseAttribute."""

    attribute_name: str = "fish_type"
    data_dict: dict[str, str]  # Der Fischtyp ist ein String

    def __init__(self, database_model: Any = None) -> None:
        super().__init__(attribute_name=self.attribute_name)

        if database_model:
            self.__read(fish_list=database_model.fish_list)

    def __read(self, fish_list: list[dict[str, Any]]) -> None:
        """Liest die Fischtypen aus der Fischliste und füllt data_dict."""
        for document in fish_list:
            catch_date: datetime.datetime = document["catch_date"]
            fish_type: str = document["fish_type"]

            formatted_string: str = catch_date.strftime(config.CATCH_DATE_FORMAT)

            self.data_dict[formatted_string] = fish_type
