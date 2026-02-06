import csv
import datetime

from fishing_analyzer import config, utils
from fishing_analyzer.data.cache import DataCache
from fishing_analyzer.data.environment.base_attribute import BaseAttribute


class PrecipitationAmountDay(BaseAttribute):
    """Repräsentiert die tägliche Niederschlagsmenge, abgeleitet von BaseAttribute.

    Beachtet, dass die tägliche Summe für jede Stunde des Tages gespeichert wird, um Kompatibilität
    mit stündlichen Datenformaten zu gewährleisten.
    """

    file_location: str = (
        "raw_data/precipitation_amount/produkt_rr_stunde_19490101_20171231_00282.txt"
    )
    attribute_name: str = "precipitation_amount_day"
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
        """Liest die stündlichen Niederschlagsdaten aus der CSV-Datei, aggregiert sie täglich
        und füllt das data_dict mit den täglichen Summen für jede Stunde.
        """
        if not self.abs_file_location:
            print(f"Error: file_location not set for {self.attribute_name}")
            return

        daily_precipitation_sums: dict[str, float] = {}

        with open(self.abs_file_location, newline="", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";", quotechar='"')

            next(csv_reader)  # Überspringt die Kopfzeile

            for row_raw in csv_reader:
                row: tuple[str, ...] = tuple(utils.strip_row(row_raw))

                if len(row) < 7:
                    print(f"Skipping malformed row: {row_raw}")
                    continue

                station, date_str, _, precipitation_amount_str, _, _, _ = row

                if utils.has_correct_year_range(date_str) and utils.validate_row(row_raw, station):
                    try:
                        date_time: datetime.datetime = datetime.datetime.strptime(
                            date_str, "%Y%m%d%H"
                        )
                        day_format: str = date_time.strftime(config.CATCH_DAY_FORMAT)
                        precipitation_amount: float = float(precipitation_amount_str)

                        daily_precipitation_sums[day_format] = (
                            daily_precipitation_sums.get(day_format, 0.0) + precipitation_amount
                        )
                    except ValueError as e:
                        print(f"Error parsing row {row_raw}: {e}")
                        continue

        # Fülle self.data_dict mit den täglichen Summen für jede Stunde des Tages
        # Da die Originalimplementierung die tägliche Summe in jede Stunde geschrieben hat.
        if daily_precipitation_sums:
            # Annahme, dass die Stundenbereiche aus den Originaldaten stammen oder 0-23 sind
            # Hier nehmen wir einfach die stündlichen Einträge vom config.MINIMAL_BEGIN_DATE bis config.MAXIMAL_END_DATE
            # und setzen die Niederschlagsmenge für jeden Tag entsprechend

            # Es ist effizienter, direkt über die Tage zu iterieren, die wir gesammelt haben
            for day_str, daily_sum in daily_precipitation_sums.items():
                # Erzeuge für jede Stunde des Tages einen Eintrag mit der Tagessumme
                # Dies repliziert das Verhalten der ursprünglichen Implementierung
                try:
                    current_day: datetime.datetime = datetime.datetime.strptime(
                        day_str, config.CATCH_DAY_FORMAT
                    )
                    for hour in range(24):
                        hourly_date_time: datetime.datetime = current_day.replace(hour=hour)
                        formatted_string: str = hourly_date_time.strftime(config.CATCH_DATE_FORMAT)
                        self.data_dict[formatted_string] = daily_sum
                except ValueError as e:
                    print(f"Error processing daily sum for {day_str}: {e}")
                    continue
