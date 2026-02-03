# coding: utf-8

import datetime
from typing import Any, Dict, List, Optional

import config
from data.environment.base_attribute import BaseAttribute


class CatchMonth(BaseAttribute):
    """Repräsentiert den Fangmonat und -tag in einem zusammengesetzten numerischen Format, 
    abgeleitet von BaseAttribute.

    Der Wert wird als float berechnet, der den Monat und den relativen Tag innerhalb des Monats darstellt.
    """

    attribute_name: str = 'fish_catch_month'
    data_dict: Dict[str, float]

    def __init__(self, database_model: Any = None) -> None:
        super().__init__(attribute_name=self.attribute_name)

        if database_model:
            self.__read(fish_list=database_model.fish_list) # type: ignore

    def __read(self, fish_list: List[Dict[str, Any]]) -> None:
        """Liest die Fangdaten aus der Fischliste und füllt data_dict mit einem zusammengesetzten
        Monats- und Tageswert.
        """
        for document in fish_list:
            catch_date: datetime.datetime = document['catch_date']

            # Formatiert das Datum in das im config definierte Format für den Schlüssel
            formatted_string: str = catch_date.strftime(config.CATCH_DATE_FORMAT)

            catch_day: float = float(catch_date.strftime("%d"))
            catch_month_int: int = int(catch_date.strftime("%m"))

            # Hier wird ein zusammengesetzter Wert berechnet:
            # (Fangtag / Max. Tage im Monat) * Monatstag-Gewichtung + (Monat / Max. Monate) * Monat-Gewichtung
            # Im Originalcode gab es eine '12.0' Gewichtung für den Monat, die hier beibehalten wird.
            catch_day_float: float = (catch_day / 31.0) * 1.0  # Annahme: Max 31 Tage
            catch_month_float: float = (float(catch_month_int) / 12.0) * 12.0

            self.data_dict[formatted_string] = catch_month_float + catch_day_float
