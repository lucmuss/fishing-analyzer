# coding: utf-8

import datetime


def get_month_name(month_index):
    return MONTH_NAME_DICT[str(month_index)]


def get_month_days_dict():
    return_dict = dict()

    for month_index in range(1, 31 + 1):
        return_dict[month_index] = month_index

    return return_dict


def get_year_range(begin, end):
    date_time_start = datetime.datetime.strptime(begin, "%Y-%m-%d %H:00:00")
    year_start = date_time_start.strftime("%Y")
    year_start_int = int(year_start)

    date_time_end = datetime.datetime.strptime(end, "%Y-%m-%d %H:00:00")
    year_end = date_time_end.strftime("%Y")
    year_end_int = int(year_end)

    year_range = range(year_start_int, year_end_int + 1)
    year_return_list = [str(year) for year in year_range]

    return year_return_list


def get_month_name_dict():
    return_dict = dict()

    for month_index in range(1, 12 + 1):
        month_string = str(month_index)
        month_name = datetime.date(2017, month_index, 1).strftime('%B')
        return_dict[month_string] = month_name

    return return_dict


MAXIMAL_PREVIOUS_DAYS = 1

FISH_TYPES = ['Karpfen', 'Forelle', 'Brachse', 'Barbe', 'Aal', 'Hecht', 'Barsch', 'Zander']

MINIMAL_BEGIN_DATE = "2013-01-01 00:00:00"
MAXIMAL_END_DATE = "2017-12-31 00:00:00"

CATCH_DATE_FORMAT = "%Y-%m-%d %H:00:00"
CATCH_DAY_FORMAT = "%Y-%m-%d"

MINIMAL_CATCHED_FISHES = 4

HISTOGRAM_BINS = 12

STANDARD_DEVIATION_FACTOR = 3.0

STATISTIC_METHODS = ['mean', 'min', 'max', 'sum']

DEFAULT_STATISTIC_METHOD = STATISTIC_METHODS[0]

YEAR_RANGE = get_year_range(MINIMAL_BEGIN_DATE, MAXIMAL_END_DATE)

MONTH_NAME_DICT = get_month_name_dict()

MONTH_DAYS_DICT = get_month_days_dict()

DEFAULT_ATTRIBUTE = 'water_temperature'

DEFAULT_DAY = ''

DEFAULT_YEAR = '2017'

DEFAULT_MONTH = ''

DEFAULT_FISH = FISH_TYPES[0]

DATABASE_NAME = 'fish_db'

DATABASE_COLLECTION_NAME = 'fish_records'

DIAGRAM_HEIGTH = 720
DIAGRAM_WIDTH = 1280

DEFAULT_DATASET_ID = 'mussmaecher'

DATABASE_DOCUMENT = {"fish_type": '', "catch_date": '', "dataset_id": ''}
