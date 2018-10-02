import csv
import datetime
import pandas as pd
from config import MINIMAL_SERIES_START_YEAR
from config import MAXIMAL_SERIES_END_YEAR

from dataset.data_cache import DataCache


class SunHours:
    location = 'weather_data/sun_hours/produkt_sd_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    data_name = 'sun_hours'

    def __init__(self):
        self.__init_data()

    def __init_data(self):

        self.__data_dict = self.__data_cache.load_cache(self.data_name, self.__data_dict)

        if self.__data_dict:
            return True

        self.__read()

        self.__data_cache.store_cache(self.data_name, self.__data_dict)

    def get_dict(self):
        return self.__data_dict

    def get_list(self):
        items_iterator = self.__data_dict.items()
        return list(items_iterator)

    def get_series(self):
        data_values = list(self.__data_dict.values())
        index_values = list(self.__data_dict.keys())
        series = pd.Series(data_values, index=index_values, name=self.data_name)

        reduced_series = series[MINIMAL_SERIES_START_YEAR:MAXIMAL_SERIES_END_YEAR]
        return reduced_series

    def __read(self):
        with open(self.location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, date, typ, sun_minutes, error = row
                station, date, typ, sun_minutes, error = station.strip(), date.strip(), typ.strip(), sun_minutes.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%Y-%m-%d %H:00:00")
                    sun_minutes = float(sun_minutes)

                    if sun_minutes:
                        sun_minutes = sun_minutes / 60.0

                    if formatted_string in self.__data_dict:
                        self.__data_dict[formatted_string] += sun_minutes
                    else:
                        self.__data_dict[formatted_string] = sun_minutes
