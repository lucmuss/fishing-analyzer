import datetime
import os

import colorlover


def get_month_name(month_index: int) -> str:
    """Gibt den Monatsnamen basierend auf dem Index zurück."""
    return MONTH_NAME_DICT[str(month_index)]


def get_month_days_dict() -> dict[int, int]:
    """Gibt ein Dictionary mit Monatsindizes und der Anzahl der Tage im Monat zurück (vereinfacht).

    Diese Funktion ist hier vereinfacht und gibt für jeden Monat die Tage 1-31 zurück.
    Für eine genauere Implementierung müsste das Jahr berücksichtigt werden.
    """
    return_dict: dict[int, int] = dict()

    # Die ursprüngliche Implementierung war fehlerhaft und wies jedem Monat
    # die Zahlen 1-31 zu. Hier wird nur ein Platzhalter erstellt.
    for month_index in range(1, 12 + 1):
        return_dict[month_index] = (
            31  # Platzhalter, da die genaue Tageanzahl vom Monat und Jahr abhängt
        )

    return return_dict


def get_year_range(begin: str, end: str) -> list[str]:
    """Extrahiert eine Liste von Jahren als Strings aus einem Datumsbereich.

    Args:
        begin: Das Startdatum im Format "YYYY-MM-DD HH:MM:SS".
        end: Das Enddatum im Format "YYYY-MM-DD HH:MM:SS".

    Returns:
        Eine Liste von Jahren als Strings, z.B. ['2013', '2014', '2015'].
    """
    date_time_start = datetime.datetime.strptime(begin, "%Y-%m-%d %H:00:00")
    year_start_int = date_time_start.year

    date_time_end = datetime.datetime.strptime(end, "%Y-%m-%d %H:00:00")
    year_end_int = date_time_end.year

    year_range = range(year_start_int, year_end_int + 1)
    year_return_list = [str(year) for year in year_range]

    return year_return_list


def get_month_name_dict() -> dict[str, str]:
    """Gibt ein Dictionary mit Monatsindizes (als String) und Monatsnamen zurück.

    Returns:
        Ein Dictionary, z.B. {'1': 'January', '2': 'February', ...}.
    """
    return_dict: dict[str, str] = dict()

    for month_index in range(1, 12 + 1):
        month_string = str(month_index)
        month_name = datetime.date(2017, month_index, 1).strftime("%B")
        return_dict[month_string] = month_name

    return return_dict


def get_color_dict(attribute_list: list[str]) -> dict[str, tuple[int, int, int]]:
    """Gibt ein Dictionary zurück, das Attributen Farben zuordnet.

    Args:
        attribute_list: Eine Liste von Attributnamen (Strings).

    Returns:
        Ein Dictionary, bei dem die Schlüssel Attributnamen sind und die Werte RGB-Farb-Tupel.
    """
    number = len(attribute_list)

    # color_scale = colorlover.scales['11']['div']['Spectral']

    color_scale = colorlover.scales["9"]["seq"]["Blues"]
    color_scale = color_scale[6:]
    color_interp = colorlover.interp(color_scale, number)

    # Sicherstellen, dass color_interp eine Liste von Hex-Farben ist, wie von colorlover.to_rgb erwartet
    color_list_hex = color_interp if isinstance(color_interp, list) else [color_interp]
    color_list_rgb: list[tuple[int, int, int]] = []
    for hex_color in colorlover.to_rgb(color_list_hex):
        value = hex_color.lstrip("#")
        rgb = (
            int(value[0:2], 16),
            int(value[2:4], 16),
            int(value[4:6], 16),
        )
        color_list_rgb.append(rgb)

    return_dict = dict(zip(attribute_list, color_list_rgb))
    return return_dict


RUN_AS_PRODUCTION: bool = os.getenv("RUN_AS_PRODUCTION", "false").lower() == "true"
MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

ATTRIBUTE_COLOR_DICT: dict = dict()

MAXIMAL_PREVIOUS_DAYS: int = 1

FISH_TYPES: list[str] = [
    "Karpfen",
    "Forelle",
    "Brachse",
    "Barbe",
    "Aal",
    "Hecht",
    "Barsch",
    "Zander",
    "Wels",
    "Schleie",
    "Döbel",
    "Äsche",
    "Bachforelle",
    "Bachsaibling",
    "Gründling",
    "Karausche",
    "Nase",
    "Rapfen",
    "Rotauge",
    "Rotfeder",
    "Rutte",
]

DEFAULT_FISH_TYPE: str = FISH_TYPES[0]

MINIMAL_BEGIN_DATE: str = "2013-01-01 00:00:00"

MAXIMAL_END_DATE: str = "2017-12-31 00:00:00"

CATCH_DATE_FORMAT: str = "%Y-%m-%d %H:00:00"

CATCH_DAY_FORMAT: str = "%Y-%m-%d"

MINIMAL_CATCHED_FISHES: int = 4

HISTOGRAM_BINS: int = 12

STANDARD_DEVIATION_FACTOR: float = 3.0

STATISTIC_METHODS: list[str] = ["mean", "min", "max", "sum"]

DEFAULT_STATISTIC_METHOD: str = STATISTIC_METHODS[0]

YEAR_RANGE: list[str] = get_year_range(MINIMAL_BEGIN_DATE, MAXIMAL_END_DATE)

MINIMAL_YEAR_RANGE_INT: int = int(YEAR_RANGE[0])

MONTH_NAME_DICT: dict[str, str] = get_month_name_dict()

MONTH_DAYS_DICT: dict[int, int] = get_month_days_dict()

DEFAULT_ATTRIBUTE: str = "water_temperature"

DEFAULT_DAY: str = ""

DEFAULT_YEAR: str = "2017"

DEFAULT_MONTH: str = ""

DATABASE_NAME: str = "fish_database"

DATABASE_FISH_COLLECTION_NAME: str = "fish_records"

DATABASE_ENVIRONMENT_COLLECTION_NAME: str = "environment_records"

DIAGRAM_HEIGTH: int = 720

DIAGRAM_WIDTH: int = 1280

FISHER_IDS: list[str] = [
    "PrivatMussmaecher",
    "PrivatKeinAngabe",
    "AngelVereinBaunach",
    "AngelVereinEbern",
    "AngelVereinPfaffendorf",
    "AngelVereinErmershausen",
    "AngelVereinBreitengüßbach",
]

DEFAULT_FISHER_ID: str = FISHER_IDS[0]

DEFAULT_CATCH_DATE: str = "2018-06-05"

DEFAULT_CATCH_HOUR: str = "17:30"

RIVER_IDS: list[str] = ["Baunach", "Itz", "Main", "Weisach", "Preppach"]

DEFAULT_RIVER_ID: str = RIVER_IDS[0]

OS_SEPARATOR: str = os.path.sep

BASE_DIRECTORY: str = os.path.dirname(__file__)

FISH_DATA_CSV_LOCATION: str = os.path.join(BASE_DIRECTORY, "data", "fish_database.csv")

DATABASE_DOCUMENT: dict[str, str] = {
    "fish_type": "",
    "catch_date": "",
    "fisher_id": "",
    "river_id": "",
}
