import csv
import datetime
import pandas
import config
import os

from data.cache.cache import DataCache


class WaterTemperature:
    location = 'raw_data/water_temperature/wassertemperatur_603100044.csv'
    __data_cache = DataCache()
    __data_dict = dict()
    attribute_name = 'water_temperature'

    def __init__(self):
        self.__init_data()

    def __init_data(self):

        self.__data_dict = self.__data_cache.load_cache(self.attribute_name, self.__data_dict)

        if self.__data_dict:
            return True

        self.__read()

        self.__data_cache.store_cache(self.attribute_name, self.__data_dict)

    @property
    def series(self):
        data_values = list(self.__data_dict.values())
        index_values = list(self.__data_dict.keys())
        series = pandas.Series(data_values, index=index_values, name=self.attribute_name)

        reduced_series = series[config.MINIMAL_SERIES_START_YEAR:config.MAXIMAL_SERIES_END_YEAR]
        return reduced_series

    def __read(self):
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, self.location)

        with open(abs_file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            for row in csv_reader:
                if len(row) >= 3 and row[2] == "Rohdaten":
                    date, temp, typ = row
                    date_time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    replaced_temp = temp.replace(',', '.')

                    if not replaced_temp:
                        replaced_temp = "0.0"
                    float_temp = float(replaced_temp)

                    self.__data_dict[formatted_string] = float_temp
