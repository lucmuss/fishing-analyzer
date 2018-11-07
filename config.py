# coding: utf-8

import datetime
import colorlover


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


def get_color_dict(attribute_list):
    number = len(attribute_list)

    # color_scale = colorlover.scales['11']['div']['Spectral']

    color_scale = colorlover.scales['9']['seq']['Blues']
    color_scale = color_scale[6:]
    color_interp = colorlover.interp(color_scale, number)
    color_list = colorlover.to_rgb(color_interp)

    return_dict = dict(zip(attribute_list, color_list))
    return return_dict



RUN_AS_PRODUCTION = True

ATTRIBUTE_COLOR_DICT = dict()

MAXIMAL_PREVIOUS_DAYS = 1

FISH_TYPES = ['Karpfen', 'Forelle', 'Brachse',
              'Barbe', 'Aal', 'Hecht',
              'Barsch', 'Zander', 'Wels',
              'Schleie', 'Döbel', 'Äsche',
              'Bachforelle', 'Bachsaibling', 'Gründling',
              'Karausche', 'Nase', 'Rapfen',
              'Rotauge', 'Rotfeder', 'Rutte',
              ]

DEFAULT_FISH_TYPE = FISH_TYPES[0]

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

MINIMAL_YEAR_RANGE_INT = int(YEAR_RANGE[0])

MONTH_NAME_DICT = get_month_name_dict()

MONTH_DAYS_DICT = get_month_days_dict()

DEFAULT_ATTRIBUTE = 'water_temperature'

DEFAULT_DAY = ''

DEFAULT_YEAR = '2017'

DEFAULT_MONTH = ''

DATABASE_NAME = 'fish_database'

DATABASE_FISH_COLLECTION_NAME = 'fish_records'

DATABASE_ENVIRONMENT_COLLECTION_NAME = 'environment_records'

DIAGRAM_HEIGTH = 720

DIAGRAM_WIDTH = 1280

FISHER_IDS = ['PrivatMussmaecher', 'PrivatKeinAngabe', 'AngelVereinBaunach',
              'AngelVereinEbern', 'AngelVereinPfaffendorf',
              'AngelVereinErmershausen', 'AngelVereinBreitengüßbach']

DEFAULT_FISHER_ID = FISHER_IDS[0]

DEFAULT_CATCH_DATE = '2018-06-05'

DEFAULT_CATCH_HOUR = '17:30'

RIVER_IDS = ['Baunach', 'Itz', 'Main', 'Weisach', 'Preppach']

DEFAULT_RIVER_ID = RIVER_IDS[0]

DATABASE_DOCUMENT = {'fish_type': '', 'catch_date': '', 'fisher_id': '', 'river_id': ''}
