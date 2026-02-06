import csv
import datetime

from fishing_analyzer import config, utils
from fishing_analyzer.data.cache import DataCache
from fishing_analyzer.data.environment.base_attribute import BaseAttribute


class PrecipitationAmount(BaseAttribute):
    """Hourly precipitation amount values."""

    file_location: str = (
        "raw_data/precipitation_amount/produkt_rr_stunde_19490101_20171231_00282.txt"
    )
    attribute_name: str = "precipitation_amount"
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
        if not self.abs_file_location:
            print(f"Error: file_location not set for {self.attribute_name}")
            return

        with open(self.abs_file_location, newline="", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";", quotechar='"')
            next(csv_reader)

            for row_raw in csv_reader:
                row: tuple[str, ...] = tuple(utils.strip_row(row_raw))
                if len(row) < 7:
                    continue

                station, date_str, _, precipitation_amount_str, _, _, _ = row
                if not (
                    utils.has_correct_year_range(date_str) and utils.validate_row(row_raw, station)
                ):
                    continue

                try:
                    date_time = datetime.datetime.strptime(date_str, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)
                    precipitation_amount = float(precipitation_amount_str)
                except ValueError:
                    continue

                if formatted_string in self.data_dict:
                    self.data_dict[formatted_string] += precipitation_amount
                else:
                    self.data_dict[formatted_string] = precipitation_amount
