import datetime
from typing import Any

from fishing_analyzer import config
from fishing_analyzer.data.environment.base_attribute import BaseAttribute


class CatchHour(BaseAttribute):
    """Repräsentiert die Fangstunde von Fischen, abgeleitet von BaseAttribute."""

    attribute_name: str = "fish_catch_hour"
    data_dict: dict[str, float]

    def __init__(self, database_model: Any = None) -> None:
        super().__init__(attribute_name=self.attribute_name)

        if database_model:
            self.__read(fish_list=database_model.fish_list)

    def __read(self, fish_list: list[dict[str, Any]]) -> None:
        """Liest die Fangstunden aus der Fischliste und füllt data_dict."""
        for document in fish_list:
            catch_date: datetime.datetime = document["catch_date"]

            # Formatiert das Datum in das im config definierte Format für den Schlüssel
            formatted_string: str = catch_date.strftime(config.CATCH_DATE_FORMAT)
            # Extrahiert die Stunde und konvertiert sie in einen Float
            catch_hour: float = float(catch_date.strftime("%H"))

            self.data_dict[formatted_string] = catch_hour
