import csv
import datetime
import pandas as pd

from config import MINIMAL_SERIES_START_YEAR
from config import MAXIMAL_SERIES_END_YEAR


class CatchHour:
    location = 'fish_data/fish_database.csv'
    data_name = 'fish_catch_hour'

    __data_dict = dict()
    __fish_catch_values = list()

    def __init__(self):
        self.__init_data()

    def __init_data(self):

        if self.__data_dict:
            return True

        self.__read()

    def get_dict(self):
        return self.__data_dict

    def get_list(self):
        items_iterator = self.__data_dict.items()
        return list(items_iterator)

    def get_series(self):
        data_values = list(self.__data_dict.values())
        index_values = list(self.__data_dict.keys())
        series = pd.Series(data_values, index=index_values, name=self.data_name)
        series = series.sort_index()

        reduced_series = series[MINIMAL_SERIES_START_YEAR:MAXIMAL_SERIES_END_YEAR]
        return reduced_series

    def __read(self):
        with open(self.location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                fish_type, date, hour = row
                fish_type, date, hour = fish_type.strip(), date.strip(), hour.strip()

                if len(row) >= 3:
                    full_date_string = date + "-" + hour

                    date_time = datetime.datetime.strptime(full_date_string, "%d.%m.%Y-%H:%M:%S")

                    formatted_string = date_time.strftime("%Y-%m-%d %H:00:00")
                    catch_hour = date_time.strftime("%H")

                    self.__data_dict[formatted_string] = catch_hour
