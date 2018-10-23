# coding: utf-8

import csv
import datetime
import config

import utils
from data.environment.base_attribute import BaseAttribute


class SunHours(BaseAttribute):
    file_location = 'raw_data/sun_hours/produkt_sd_stunde_19490101_20171231_00282.txt'
    attribute_name = 'sun_hours'

    def __init__(self, data_cache=None):

        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               file_location=self.file_location)

        self.data_cache = data_cache
        self.data_dict = self.data_cache.load_dict(attribute_name=self.attribute_name)

        if not self.data_dict:
            self.__read()
            self.data_cache.store_dict(attribute_name=self.attribute_name, store_dict=self.data_dict)

    def __read(self):

        day_dict = dict()

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, sun_minutes, error = utils.strip_row(row)

                if utils.validate_row(row, station):

                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")

                    day_format = date_time.strftime(config.CATCH_DAY_FORMAT)
                    sun_minutes = float(sun_minutes)

                    if day_format in day_dict:
                        day_dict[day_format] += sun_minutes
                    else:
                        day_dict[day_format] = sun_minutes

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, sun_minutes, error = utils.strip_row(row)

                if utils.validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")

                    date_format = date_time.strftime(config.CATCH_DATE_FORMAT)
                    day_format = date_time.strftime(config.CATCH_DAY_FORMAT)

                    hour_value = float(day_dict[day_format]) / 60.0

                    self.data_dict[date_format] = hour_value
