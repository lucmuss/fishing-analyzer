# coding: utf-8

import pandas
import config
import os


class BaseAttribute:

    def __init__(self, location=None, attribute_name=None):
        self.attribute_name = attribute_name
        self.location = location
        self.data_dict = dict()

    @property
    def series(self):
        data_values = list(self.data_dict.values())
        index_values = list(self.data_dict.keys())
        series = pandas.Series(data_values, index=index_values, name=self.attribute_name)

        reduced_series = series[config.MINIMAL_BEGIN_DATE:config.MAXIMAL_END_DATE]
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
