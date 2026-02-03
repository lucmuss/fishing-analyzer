# coding: utf-8

import csv
import datetime
from typing import Any, Dict, Optional, Tuple, Union

import config
import utils
from data.cache import DataCache
from data.environment.base_attribute import BaseAttribute


class PrecipitationAmount(BaseAttribute):
    """Repräsentiert die Niederschlagsmengen an Daten, abgeleitet von BaseAttribute."""

    file_location: str = 'raw_data/precipitation_amount/produkt_rr_stunde_19490101_20171231_00282.txt'
    attribute_name: str = 'precipitation_amount'
    data_cache: DataCache
    data_dict: Dict[str, float]

    def __init__(self, data_cache: DataCache) -> None:
        super().__init__(attribute_name=self.attribute_name,
                         file_location=self.file_location)
        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(attribute_name=self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(attribute_name=self.attribute_name, store_dict=self.data_dict)

    def __read(self) -> None:
        """Liest die Niederschlagsmengen aus der CSV-Datei und füllt data_dict."""
        if not self.abs_file_location:
            print(f"Error: file_location not set for {self.attribute_name}")
            return

        with open(self.abs_file_location, newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)  # Überspringt die Kopfzeile

            for row_raw in csv_reader:
                row: Tuple[str, ...] = tuple(utils.strip_row(row_raw))  # type: ignore

                # Sicherstellen, dass die Zeile genügend Elemente hat
                if len(row) < 7:
                    print(f"Skipping malformed row: {row_raw}")
                    continue

                station, date_str, _, precipitation_amount_str, _, _, _ = row

                # Überprüfen, ob die Daten relevant sind (z.B. innerhalb des Jahresbereichs und gültige Station)
                if utils.has_correct_year_range(date_str) and utils.validate_row(row_raw, station):
                    try:
                        date_time: datetime.datetime = datetime.datetime.strptime(date_str, "%Y%m%d%H")
                        formatted_string: str = date_time.strftime(config.CATCH_DATE_FORMAT)
                        precipitation_amount: float = float(precipitation_amount_str)

                        # Aggregiert Niederschlagsmengen für den gleichen Zeitpunkt
                        if formatted_string in self.data_dict:
                            self.data_dict[formatted_string] += precipitation_amount
                        else:
                            self.data_dict[formatted_string] = precipitation_amount
