import csv
import datetime

from fishing_analyzer import config, utils
from fishing_analyzer.data.cache import DataCache
from fishing_analyzer.data.environment.base_attribute import BaseAttribute


class WaterTemperature(BaseAttribute):
    """Repräsentiert die Wassertemperaturdaten, abgeleitet von BaseAttribute."""

    file_location: str = "raw_data/water_temperature/wassertemperatur_603100044.csv"
    attribute_name: str = "water_temperature"
    data_cache: DataCache
    data_dict: dict[str, float]

    def __init__(self, data_cache: DataCache) -> None:
        super().__init__(attribute_name=self.attribute_name, file_location=self.file_location)
        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(attribute_name=self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(
                attribute_name=self.attribute_name, store_dict=self.data_dict
            )

    def __read(self) -> None:
        """Liest die Wassertemperaturdaten aus der CSV-Datei und füllt data_dict."""
        if not self.abs_file_location:
            print(f"Error: file_location not set for {self.attribute_name}")
            return

        with open(self.abs_file_location, newline="", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";", quotechar='"')

            next(csv_reader)  # Überspringt die Kopfzeile

            for row_raw in csv_reader:
                row: tuple[str, ...] = tuple(utils.strip_row(row_raw))

                if utils.validate_water_row(row_raw):
                    date_str, temp_str, _ = row

                    try:
                        date_time: datetime.datetime = datetime.datetime.strptime(
                            date_str, "%Y-%m-%d %H:%M"
                        )
                        formatted_string: str = date_time.strftime(config.CATCH_DATE_FORMAT)

                        replaced_temp: str = temp_str.replace(",", ".")

                        if not replaced_temp:
                            replaced_temp = "0.0"
                        float_temp: float = float(replaced_temp)

                        self.data_dict[formatted_string] = float_temp

                    except ValueError as e:
                        print(f"Error parsing row {row_raw}: {e}")
                        continue
