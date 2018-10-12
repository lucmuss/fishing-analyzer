import csv
import datetime
import pandas
import config
import os

from data.cache.cache import DataCache


class GroundTemperature5:
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    attribute_name = 'ground_temperature_5'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp5)

                    self.__data_dict[formatted_string] = ground_temperature


class GroundTemperature10:
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    attribute_name = 'ground_temperature_10'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp10)

                    self.__data_dict[formatted_string] = ground_temperature


class GroundTemperature20:
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    attribute_name = 'ground_temperature_20'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp20)

                    self.__data_dict[formatted_string] = ground_temperature


class GroundTemperature50:
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    attribute_name = 'ground_temperature_50'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp50)

                    self.__data_dict[formatted_string] = ground_temperature


class GroundTemperature100:
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    attribute_name = 'ground_temperature_100'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp100)

                    self.__data_dict[formatted_string] = ground_temperature
