# coding: utf-8

from utils import get_month_name_dict, get_year_range, get_month_days_dict

MAXIMAL_PREVIOUS_DAYS = 1

FISH_TYPES = ['Karpfen', 'Forelle', 'Brachse', 'Barbe', 'Aal', 'Hecht', 'Barsch', 'Zander']

MINIMAL_BEGIN_DATE = "2013-01-01 00:00:00"
MAXIMAL_END_DATE = "2017-12-31 00:00:00"

CATCH_DATE_FORMAT = "%Y-%m-%d %H:00:00"
CATCH_DAY_FORMAT = "%Y-%m-%d"

MINIMAL_CATCHED_FISHES = 2

HISTOGRAM_BINS = 20

STANDARD_DEVIATION_FACTOR = 3.0

YEAR_RANGE = get_year_range()

MONTH_NAME_DICT = get_month_name_dict()

MONTH_DAYS_DICT = get_month_days_dict()

DEFAULT_ATTRIBUTE = 'water_temperature'

DEFAULT_DAY = ''

DEFAULT_YEAR = '2017'

DEFAULT_MONTH = ''

DATABASE_NAME = 'fish_db'

DATABASE_COLLECTION_NAME = 'fish_records'

DIAGRAM_HEIGTH = 720
DIAGRAM_WIDTH = 1280

DEFAULT_DATASET_ID = 'mussmaecher'

DATABASE_DOCUMENT = {"fish_type": '', "catch_date": '', "dataset_id": ''}
