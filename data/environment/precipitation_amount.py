# coding: utf-8

import csv
import datetime
import config

import utils
from data.environment.base_attribute import BaseAttribute


class PrecipitationAmount(BaseAttribute):
    location = 'raw_data/precipitation_amount/produkt_rr_stunde_19490101_20171231_00282.txt'
    attribute_name = 'precipitation_amount'

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

                station, date, typ, precipitation_amount, a, b, error = utils.strip_row(row)

                if utils.validate_row(row, station):
                    date_time = datetime.datetime.strptime(date, "%Y%m%d%H")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)
                    precipitation_amount = float(precipitation_amount)

                    if formatted_string in self.data_dict:
                        self.data_dict[formatted_string] += precipitation_amount
                    else:
                        self.data_dict[formatted_string] = precipitation_amount
