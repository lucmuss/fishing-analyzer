import datetime
from typing import Any, Dict, List, Optional

from fishing_analyzer import config
from fishing_analyzer.data.environment.base_attribute import BaseAttribute


class CatchDate(BaseAttribute):
    """Repräsentiert das Fangdatum von Fischen, abgeleitet von BaseAttribute."""

    attribute_name: str = "fish_catch_date"
    data_dict: dict[str, str]

    def __init__(self, database_model: Any = None) -> None:
        super().__init__(attribute_name=self.attribute_name)

        if database_model:
            self.__read(fish_list=database_model.fish_list)  # type: ignore

    def __read(self, fish_list: list[dict[str, Any]]) -> None:
        """Liest die Fangdaten aus der Fischliste und füllt data_dict."""
        for document in fish_list:
            catch_date: datetime.datetime = document["catch_date"]

            # Formatiert das Datum in das im config definierte Format für den Schlüssel
            formatted_string: str = catch_date.strftime(config.CATCH_DATE_FORMAT)
            # Speichert das Datum im Format YYYY-MM-DD als Wert
            catch_date_str: str = catch_date.strftime("%Y-%m-%d")

            self.data_dict[formatted_string] = catch_date_str
