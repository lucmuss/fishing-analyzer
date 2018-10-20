# coding: utf-8

import pandas
import config


class FishType:
    attribute_name = 'fish_type'

    __data_dict = dict()

    def __init__(self, database_model=None):
        self.__read(database_model.fish_list)

    @property
    def series(self):
        data_values = list(self.__data_dict.values())
        index_values = list(self.__data_dict.keys())
        series = pandas.Series(data_values, index=index_values, name=self.attribute_name)
        series = series.sort_index()

        reduced_series = series[config.MINIMAL_BEGIN_DATE:config.MAXIMAL_END_DATE]
        return reduced_series

    def __read(self, fish_list):
        for document in fish_list:
            catch_date = document['catch_date']
            fish_type = document['fish_type']

            formatted_string = catch_date.strftime(config.CATCH_DATE_FORMAT)

            self.__data_dict[formatted_string] = fish_type
