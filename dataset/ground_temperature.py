import csv
import datetime
import pandas as pd
from settings import MINIMAL_SERIES_START_YEAR
from settings import MAXIMAL_SERIES_END_YEAR

from dataset.data_cache import DataCache


class GroundTemperature5:
    location = 'weather_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    data_name = 'ground_temperature_5'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%Y-%m-%d %H:00:00")

                    ground_temperature = float(temp5)

                    self.__data_dict[formatted_string] = ground_temperature


class GroundTemperature10:
    location = 'weather_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    data_name = 'ground_temperature_10'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%Y-%m-%d %H:00:00")

                    ground_temperature = float(temp10)

                    self.__data_dict[formatted_string] = ground_temperature


class GroundTemperature20:
    location = 'weather_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    data_name = 'ground_temperature_20'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%Y-%m-%d %H:00:00")

                    ground_temperature = float(temp20)

                    self.__data_dict[formatted_string] = ground_temperature


class GroundTemperature50:
    location = 'weather_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    data_name = 'ground_temperature_50'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%Y-%m-%d %H:00:00")

                    ground_temperature = float(temp50)

                    self.__data_dict[formatted_string] = ground_temperature


class GroundTemperature100:
    location = 'weather_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    __data_cache = DataCache()
    __data_dict = dict()
    data_name = 'ground_temperature_100'

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

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = row
                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100 = station.strip(), date.strip(), typ.strip(), temp2.strip(), temp5.strip(), temp10.strip(), temp20.strip(), temp50.strip(), temp100.strip()

                if len(row) >= 5 and station == "282":
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime("%Y-%m-%d %H:00:00")

                    ground_temperature = float(temp100)

                    self.__data_dict[formatted_string] = ground_temperature
