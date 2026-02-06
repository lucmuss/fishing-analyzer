import csv
import datetime
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from fishing_analyzer import config, utils
from fishing_analyzer.data.cache import DataCache
from fishing_analyzer.data.environment.base_attribute import BaseAttribute


class GroundTemperatureBase(BaseAttribute):
    """Basisklasse für Bodentemperaturdaten in verschiedenen Tiefen."""

    file_location: str = "raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt"
    _depth_index: int
    data_cache: DataCache
    data_dict: dict[str, float]

    def __init__(self, data_cache: DataCache, attribute_name: str, depth_index: int) -> None:
        super().__init__(attribute_name=attribute_name, file_location=self.file_location)
        self.data_cache = data_cache
        self._depth_index = depth_index
        self.data_dict = self.data_cache.load_dict(attribute_name=attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(attribute_name=attribute_name, store_dict=self.data_dict)

    def __read(self) -> None:
        """Liest Bodentemperaturdaten aus der CSV-Datei und füllt data_dict."""
        if not self.abs_file_location:
            print(f"Error: file_location not set for {self.attribute_name}")
            return

        with open(self.abs_file_location, newline="", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";", quotechar='"')

            next(csv_reader)  # Überspringt die Kopfzeile

            for row_raw in csv_reader:
                row: tuple[str, ...] = tuple(utils.strip_row(row_raw))  # type: ignore

                # Sicherstellen, dass die Zeile genügend Elemente hat
                if len(row) < 10:  # Mindestens 10 Spalten erwartet
                    print(f"Skipping malformed row: {row_raw}")
                    continue

                (
                    station,
                    date_str,
                    _,
                    temp2_str,
                    temp5_str,
                    temp10_str,
                    temp20_str,
                    temp50_str,
                    temp100_str,
                    _,
                ) = row  # type: ignore

                if utils.has_correct_year_range(date_str) and utils.validate_row(row_raw, station):  # type: ignore
                    try:
                        date_time: datetime.datetime = datetime.datetime.strptime(
                            date_str, "%Y%m%d%H"
                        )
                        formatted_string: str = date_time.strftime(config.CATCH_DATE_FORMAT)

                        # Extrahiere die Temperatur basierend auf _depth_index
                        ground_temperature_str: str
                        if self._depth_index == 2:
                            ground_temperature_str = temp2_str
                        elif self._depth_index == 5:
                            ground_temperature_str = temp5_str
                        elif self._depth_index == 10:
                            ground_temperature_str = temp10_str
                        elif self._depth_index == 20:
                            ground_temperature_str = temp20_str
                        elif self._depth_index == 50:
                            ground_temperature_str = temp50_str
                        elif self._depth_index == 100:
                            ground_temperature_str = temp100_str
                        else:
                            continue  # Ungültiger Tiefenindex

                        ground_temperature: float = float(ground_temperature_str)
                        self.data_dict[formatted_string] = ground_temperature
                    except ValueError as e:
                        print(f"Error parsing row {row_raw}: {e}")
                        continue


class GroundTemperature2(GroundTemperatureBase):
    """Bodentemperatur in 2 cm Tiefe."""

    def __init__(self, data_cache: DataCache) -> None:
        super().__init__(data_cache, "ground_temperature_2", depth_index=2)


class GroundTemperature5(GroundTemperatureBase):
    """Bodentemperatur in 5 cm Tiefe."""

    def __init__(self, data_cache: DataCache) -> None:
        super().__init__(data_cache, "ground_temperature_5", depth_index=5)


class GroundTemperature10(GroundTemperatureBase):
    """Bodentemperatur in 10 cm Tiefe."""

    def __init__(self, data_cache: DataCache) -> None:
        super().__init__(data_cache, "ground_temperature_10", depth_index=10)


class GroundTemperature20(GroundTemperatureBase):
    """Bodentemperatur in 20 cm Tiefe."""

    def __init__(self, data_cache: DataCache) -> None:
        super().__init__(data_cache, "ground_temperature_20", depth_index=20)


class GroundTemperature50(GroundTemperatureBase):
    """Bodentemperatur in 50 cm Tiefe."""

    def __init__(self, data_cache: DataCache) -> None:
        super().__init__(data_cache, "ground_temperature_50", depth_index=50)


class GroundTemperature100(GroundTemperatureBase):
    """Bodentemperatur in 100 cm Tiefe."""

    def __init__(self, data_cache: DataCache) -> None:
        super().__init__(data_cache, "ground_temperature_100", depth_index=100)
