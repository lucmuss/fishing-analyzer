# coding: utf-8

import csv
import datetime
import config

import utils
from data.environment.base_attribute import BaseAttribute


class GroundTemperature2(BaseAttribute):
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    attribute_name = 'ground_temperature_2'

    def __init__(self, data_cache=None):

        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               location=self.location)

        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(self.attribute_name, self.data_dict)

    def __read(self):

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = utils.strip_row(row)

                if utils.validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp2)

                    self.data_dict[formatted_string] = ground_temperature


class GroundTemperature5(BaseAttribute):
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    attribute_name = 'ground_temperature_5'

    def __init__(self, data_cache=None):

        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               location=self.location)

        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(self.attribute_name, self.data_dict)

    def __read(self):

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = utils.strip_row(row)

                if utils.validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp5)

                    self.data_dict[formatted_string] = ground_temperature


class GroundTemperature10(BaseAttribute):
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    attribute_name = 'ground_temperature_10'

    def __init__(self, data_cache=None):

        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               location=self.location)

        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(self.attribute_name, self.data_dict)

    def __read(self):

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = utils.strip_row(row)

                if utils.validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp10)

                    self.data_dict[formatted_string] = ground_temperature


class GroundTemperature20(BaseAttribute):
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    attribute_name = 'ground_temperature_20'

    def __init__(self, data_cache=None):

        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               location=self.location)

        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(self.attribute_name, self.data_dict)

    def __read(self):

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = utils.strip_row(row)

                if utils.validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp20)

                    self.data_dict[formatted_string] = ground_temperature


class GroundTemperature50(BaseAttribute):
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    attribute_name = 'ground_temperature_50'

    def __init__(self, data_cache=None):

        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               location=self.location)

        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(self.attribute_name, self.data_dict)

    def __read(self):

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = utils.strip_row(row)

                if utils.validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp50)

                    self.data_dict[formatted_string] = ground_temperature


class GroundTemperature100(BaseAttribute):
    location = 'raw_data/ground_temperature/produkt_eb_stunde_19490101_20171231_00282.txt'
    attribute_name = 'ground_temperature_100'

    def __init__(self, data_cache=None):

        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               location=self.location)

        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(self.attribute_name, self.data_dict)

    def __read(self):

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, temp2, temp5, temp10, temp20, temp50, temp100, e = utils.strip_row(row)

                if utils.validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    ground_temperature = float(temp100)

                    self.data_dict[formatted_string] = ground_temperature
