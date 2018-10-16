# coding: utf-8

from utils import get_month_dict, get_year_list, get_day_dict

MAX_PREVIOUS_DAYS = 1

ALLOWED_FISH_TYPES = ['Karpfen', 'Forelle', 'Brachse', 'Barbe', 'Aal', 'Hecht', 'Barsch', 'Zander']

MINIMAL_SERIES_START_YEAR = "2013-01-01 00:00:00"
MAXIMAL_SERIES_END_YEAR = "2017-12-31 00:00:00"

CATCH_DATE_FORMAT = "%Y-%m-%d %H:00:00"

MINIMAL_CATCHED_FISHES = 2

HISTOGRAM_BINS = 20

STANDARD_DEVIATION_FACTOR = 3.0

YEAR_LIST = get_year_list()

MONTH_DICT = get_month_dict()

MONTH_DAYS_DICT = get_day_dict()

DEFAULT_ATTRIBUTE = 'water_temperature'

DEFAULT_DAY = ''

DEFAULT_YEAR = '2017'

DEFAULT_MONTH = ''

DATABASE_NAME = 'fish_db'

DATABASE_COLLECTION_NAME = 'fish_records'

DIAGRAM_HEIGTH = 720
DIAGRAM_WIDTH = 1280
