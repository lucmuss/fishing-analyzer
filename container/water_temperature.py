import csv
import datetime
import pandas as pd
from settings import MINIMAL_SERIES_START_YEAR
from settings import MAXIMAL_SERIES_END_YEAR

from container.data_cache import DataCache


class WaterTemperature:
    location = 'weather_data/water_temperature/wassertemperatur_603100044.csv'
    __data_cache = DataCache()
    __water_temperature = dict()

    def __init__(self):
        self.__init_data()

    def __init_data(self):

        self.__water_temperature = self.__data_cache.load_cache('water_temperature', self.__water_temperature)

        if self.__water_temperature:
            return True

        self.__read()

        self.__data_cache.store_cache('water_temperature', self.__water_temperature)

    def get_dict(self):
        return self.__water_temperature

    def get_list(self):
        items_iterator = self.__water_temperature.items()
        return list(items_iterator)

    def get_series(self):
        data_values = list(self.__water_temperature.values())
        index_values = list(self.__water_temperature.keys())
        series = pd.Series(data_values, index=index_values, name='water_temperature')

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

                    self.__water_temperature[formatted_string] = float_temp

