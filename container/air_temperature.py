import csv
import datetime
import pandas as pd
from settings import MINIMAL_SERIES_START_YEAR
from settings import MAXIMAL_SERIES_END_YEAR

from container.data_cache import DataCache


class AirTemperature:
    location = 'weather_data/relativ_humidity_air_temperature/produkt_tu_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __air_temperature = dict()

    def __init__(self):
        self.__init_data()

    def __init_data(self):

        self.__air_temperature = self.__data_cache.load_cache('air_temperature', self.__air_temperature)

        if self.__air_temperature:
            return True

        self.__read()

        self.__data_cache.store_cache('air_temperature', self.__air_temperature)

    def get_dict(self):
        return self.__air_temperature

    def get_list(self):
        items_iterator = self.__air_temperature.items()
        return list(items_iterator)

    def get_series(self):
        data_values = list(self.__air_temperature.values())
        index_values = list(self.__air_temperature.keys())
        series = pd.Series(data_values, index=index_values, name='air_temperature')

        reduced_series = series[MINIMAL_SERIES_START_YEAR:MAXIMAL_SERIES_END_YEAR]
        return reduced_series

    def __read(self):
        with open(self.location,
                  newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:

                station, date, typ, temperature, humidity, error = row
                station, date, typ, temperature, humidity, error = station.strip(), date.strip(), typ.strip(), temperature.strip(), humidity.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%Y-%m-%d %H:00:00")

                    float_temp = float(temperature)
                    self.__air_temperature[formatted_string] = float_temp
