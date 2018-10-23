# coding: utf-8

import csv
import datetime
import config

import utils
from data.environment.base_attribute import BaseAttribute


class WaterTemperature(BaseAttribute):
    file_location = 'raw_data/water_temperature/wassertemperatur_603100044.csv'
    attribute_name = 'water_temperature'

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

                if utils.validate_water_row(row):

                    date, temp, typ = utils.strip_row(row)

                    date_time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
                    formatted_string = date_time.strftime(config.CATCH_DATE_FORMAT)

                    replaced_temp = temp.replace(',', '.')

                    if not replaced_temp:
                        replaced_temp = "0.0"
                    float_temp = float(replaced_temp)

                    self.data_dict[formatted_string] = float_temp
