# coding: utf-8

import csv
import datetime
import config

import utils
from data.environment.base_attribute import BaseAttribute


class WindStrength(BaseAttribute):
    file_location = 'raw_data/wind_strength/produkt_ff_stunde_19490101_20171231_00282.txt'
    attribute_name = 'wind_strength'

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

        with open(self.abs_file_location, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')

            next(csv_reader)

            for row in csv_reader:

                station, date, typ, strength, direction, a = utils.strip_row(row)

                if utils.has_correct_year_range(date):
                    if utils.validate_row(row, station):
                        date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                        formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                        wind_strength = float(strength)
                        self.data_dict[formatted_string] = wind_strength
