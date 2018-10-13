import datetime

MAX_PREVIOUS_DAYS = 1

ALLOWED_FISH_TYPES = ['Karpfen', 'Forelle', 'Brachse', 'Barbe', 'Aal', 'Hecht', 'Barsch', 'Zander']

MINIMAL_SERIES_START_YEAR = "2013-01-01 00:00:00"
MAXIMAL_SERIES_END_YEAR = "2017-12-31 00:00:00"

CATCH_DATE_FORMAT = "%Y-%m-%d %H:00:00"

MINIMAL_CATCHED_FISHES = 2

HISTOGRAM_BINS = 20

STANDARD_DEVIATION_FACTOR = 3.0


def get_year_list():
    date_time_start = datetime.datetime.strptime(MINIMAL_SERIES_START_YEAR, "%Y-%m-%d %H:00:00")
    year_start = date_time_start.strftime("%Y")
    year_start_int = int(year_start)

    date_time_end = datetime.datetime.strptime(MAXIMAL_SERIES_END_YEAR, "%Y-%m-%d %H:00:00")
    year_end = date_time_end.strftime("%Y")
    year_end_int = int(year_end)

    year_range = range(year_start_int, year_end_int + 1)
    year_return_list = [str(year) for year in year_range]

    return year_return_list


YEAR_LIST = get_year_list()


def get_month_dict():
    return_dict = dict()

    for month_index in range(1, 12 + 1):
        month_string = str(month_index)
        month_name = datetime.date(2017, month_index, 1).strftime('%B')
        return_dict[month_string] = month_name

    return return_dict


MONTH_DICT = get_month_dict()


def get_day_dict():
    return_dict = dict()

    for month_index in range(1, 31 + 1):
        return_dict[month_index] = month_index

    return return_dict


MONTH_DAYS_DICT = get_day_dict()

DEFAULT_ATTRIBUTE = 'water_temperature'

DEFAULT_DAY = ''

DEFAULT_YEAR = '2017'

DEFAULT_MONTH = ''

get_month_name = lambda month_index: MONTH_DICT[str(month_index)]

DATABASE_NAME = 'fish_db'

DATABASE_COLLECTION_NAME = 'fish_records'

get_database_document = lambda fish_type, catch_date,: {"fish_type": fish_type, "catch_date": catch_date}


def attribute_to_name(attribute_name):
    attribute_list = attribute_name.split('_')

    attribute_list = [attribute.title() for attribute in attribute_list]

    attribute_title = ' '.join(attribute_list)

    return attribute_title


fish_and_attribute = lambda fish_type, attribute_name: "{}: {}".format(fish_type, attribute_name)

DIAGRAM_HEIGTH = 720
DIAGRAM_WIDTH = 1280
