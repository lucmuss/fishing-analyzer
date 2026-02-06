import csv
import datetime
import os
from typing import Any

from fishing_analyzer import config, utils


def import_to_db(
    database_model: Any | None = None, location: str = config.FISH_DATA_CSV_LOCATION
) -> None:
    """Importiert Fischdaten aus einer CSV-Datei in die Datenbank.

    Args:
        database_model: Das Datenbankmodell, das die add_fish-Methode bereitstellt.
        location: Der Pfad zur CSV-Datei.
    """
    script_dir: str = os.path.dirname(__file__)
    abs_file_path: str = os.path.join(script_dir, location)

    if not os.path.exists(abs_file_path):
        print(f"Error: CSV file not found at {abs_file_path}")
        return

    if not database_model:
        print("Error: database_model not provided.")
        return

    with open(abs_file_path, newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";", quotechar='"')

        for row_raw in csv_reader:
            row: tuple[str, ...] = tuple(utils.strip_row(row_raw))

            if len(row) < 3:
                print(f"Skipping malformed row: {row_raw}")
                continue

            fish_type: str = row[0]
            date_str: str = row[1]
            hour_str: str = row[2]

            if fish_type in config.FISH_TYPES:
                full_date_string: str = " ".join((date_str, hour_str))

                try:
                    date_time: datetime.datetime = datetime.datetime.strptime(
                        full_date_string, "%d.%m.%Y %H:%M:%S"
                    )
                    formatted_string: str = date_time.strftime(config.CATCH_DATE_FORMAT)

                    database_model.add_fish(
                        fish_type=fish_type,
                        catch_date=formatted_string,
                        fisher_id=None,
                        river_id=None,
                    )
                except ValueError as e:
                    print(f"Error parsing date/time in row {row_raw}: {e}")
                    continue


if __name__ == "__main__":
    from fishing_analyzer.data.model import ModelFactory

    model_factory: ModelFactory = ModelFactory()
    database_model: Any = model_factory.database_model

    print("Importing data to DB...")
    import_to_db(database_model=database_model)
    print("Import finished.")
