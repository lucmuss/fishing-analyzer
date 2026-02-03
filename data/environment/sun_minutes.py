# coding: utf-8

import csv
import datetime
from typing import Any, Dict, Optional, Tuple, Union

import config
import utils
from data.cache import DataCache
from data.environment.base_attribute import BaseAttribute


class SunMinutes(BaseAttribute):
    """Repräsentiert die stündlichen Sonnenminuten, abgeleitet von BaseAttribute.

    Die Sonnenminuten werden hier in Stunden umgerechnet (Minuten / 60).
    """

    file_location: str = 'raw_data/sun_hours/produkt_sd_stunde_19490101_20171231_00282.txt'
    attribute_name: str = 'sun_minutes'
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
        """Liest die stündlichen Sonnenminuten aus der CSV-Datei, aggregiert sie gegebenenfalls
        und füllt data_dict nach Umrechnung in Stunden.
        """
        if not self.abs_file_location:
            print(f"Error: file_location not set for {self.attribute_name}")
            return

        with open(self.abs_file_location, newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)  # Überspringt die Kopfzeile

            for row_raw in csv_reader:
                row: Tuple[str, ...] = tuple(utils.strip_row(row_raw)) # type: ignore

                if len(row) < 5:
                    print(f"Skipping malformed row: {row_raw}")
                    continue

                station, date_str, _, sun_minutes_str, _ = row

                if utils.has_correct_year_range(date_str) and utils.validate_row(row_raw, station): # type: ignore
                    try:
                        date_time: datetime.datetime = datetime.datetime.strptime(date_str, "%Y%m%d%H")
                        formatted_string: str = date_time.strftime(config.CATCH_DATE_FORMAT)
                        sun_minutes: float = float(sun_minutes_str)

                        # Umrechnung von Minuten in Stunden
                        if sun_minutes: # Nur umrechnen, wenn es einen Wert gibt
                            sun_minutes = sun_minutes / 60.0

                        # Aggregiert Sonnenstunden für den gleichen Zeitpunkt
                        if formatted_string in self.data_dict:
                            self.data_dict[formatted_string] += sun_minutes
                        else:
                            self.data_dict[formatted_string] = sun_minutes
                    except ValueError as e:
                        print(f"Error parsing row {row_raw}: {e}")
                        continue
