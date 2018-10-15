import csv
import datetime
import pandas
import config
import os


class RelativeHumidity:
    location = 'raw_data/relativ_humidity_air_temperature/produkt_tu_stunde_19490101_20171231_00282.txt'

    __data_dict = dict()
    attribute_name = 'relative_humidity'

    def __init__(self, data_cache):
        self.__data_cache = data_cache
        self.__data_dict = self.__data_cache.load_dict(self.attribute_name)

        if not self.__data_dict:
            self.__read()
            self.__data_cache.store_dict(self.attribute_name, self.__data_dict)

    @property
    def series(self):
        data_values = list(self.__data_dict.values())
        index_values = list(self.__data_dict.keys())
        series = pandas.Series(data_values, index=index_values, name=self.attribute_name)

        reduced_series = series[config.MINIMAL_SERIES_START_YEAR:config.MAXIMAL_SERIES_END_YEAR]
        return reduced_series

    @property
    def abs_file_location(self):
        location_list = self.location.split('/')
        location_paths = location_list[:-1]
        location_file = location_list[len(location_list) - 1]

        script_dir = os.path.dirname(__file__)

        abs_file_path = os.path.join(script_dir, *location_paths)
        abs_file_location = os.path.join(abs_file_path, location_file)
        return abs_file_location

    def __validate_row(self, row, station):
        return len(row) >= 5 and station == "282"

    def __read(self):

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, temperature, humidity, error = config.strip_row(row)

                if self.__validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    float_humidity = float(humidity)
                    self.__data_dict[formatted_string] = float_humidity
