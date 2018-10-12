import csv
import datetime
import pandas
import config
import os

from data.cache.cache import DataCache


class SunHours:
    location = 'raw_data/sun_hours/produkt_sd_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    attribute_name = 'sun_hours'

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

                station, date, typ, sun_minutes, error = row
                station, date, typ, sun_minutes, error = station.strip(), date.strip(), typ.strip(), sun_minutes.strip(), error.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)
                    sun_minutes = float(sun_minutes)

                    if sun_minutes:
                        sun_minutes = sun_minutes / 60.0

                    if formatted_string in self.__data_dict:
                        self.__data_dict[formatted_string] += sun_minutes
                    else:
                        self.__data_dict[formatted_string] = sun_minutes
