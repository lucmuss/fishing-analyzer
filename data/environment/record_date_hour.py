import csv
import datetime
import pandas
import config
import os

from data.cache.cache import DataCache


class RecordDateHour:
    location = 'raw_data/relativ_humidity_air_temperature/produkt_tu_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    attribute_name = 'record_date_hour'

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

                station, date, typ, temperature, humidity, error = row
                station, date, typ, temperature, humidity, error = station.strip(), date.strip(), typ.strip(), temperature.strip(), humidity.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    self.__data_dict[formatted_string] = formatted_string
