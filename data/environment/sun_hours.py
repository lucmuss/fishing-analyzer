# coding: utf-8

import csv
import datetime
import config

import utils
from data.environment.base_attribute import BaseAttribute


class SunHours(BaseAttribute):
    location = 'raw_data/sun_hours/produkt_sd_stunde_19490101_20171231_00282.txt'
    attribute_name = 'sun_hours'

    def __init__(self, data_cache=None):

        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               location=self.location)

        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(self.attribute_name, self.data_dict)

    def __validate_row(self, row, station):
        return len(row) >= 5 and station == "282"

    def __read(self):

        day_dict = dict()

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, sun_minutes, error = utils.strip_row(row)

                if self.__validate_row(row, station):

                    date_time = datetime.datetime.strptime(date, "%Y%m%d")

                    formatted_string = date_time.strftime(config.CATCH_DAY_FORMAT)
                    sun_minutes = float(sun_minutes)

                    if formatted_string in day_dict:
                        day_dict[formatted_string] += sun_minutes
                    else:
                        day_dict[formatted_string] = sun_minutes

            for row in csv_reader:

                station, date, typ, sun_minutes, error = utils.strip_row(row)

                if self.__validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    day_time = datetime.datetime.strptime(date, "%Y%m%d")

                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    hour_value = float(day_dict[day_time]) / 60.0

                    self.data_dict[formatted_string] = hour_value
