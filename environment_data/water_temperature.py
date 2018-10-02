import csv
import datetime
import pandas as pd
from config import MINIMAL_SERIES_START_YEAR
from config import MAXIMAL_SERIES_END_YEAR

from environment_data.data_cache import DataCache


class WaterTemperature:
    location = 'weather_data/water_temperature/wassertemperatur_603100044.csv'
    __data_cache = DataCache()
    __data_dict = dict()
    data_name = 'water_temperature'

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
                if len(row) >= 3 and row[2] == "Rohdaten":
                    date, temp, typ = row
                    date_time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
                    formatted_string = date_time.strftime("%Y-%m-%d %H:00:00")

                    replaced_temp = temp.replace(',', '.')

                    if not replaced_temp:
                        replaced_temp = "0.0"
                    float_temp = float(replaced_temp)

                    self.__data_dict[formatted_string] = float_temp

