# coding: utf-8

import pandas
import config
from data.environment.base_attribute import BaseAttribute


class CatchHour(BaseAttribute):
    attribute_name = 'fish_catch_hour'

    def __init__(self, database_model=None):
        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               )

        self.__read(fish_list=database_model.fish_list)

    def __read(self, fish_list):
        for document in fish_list:
            catch_date = document['catch_date']

            formatted_string = catch_date.strftime(config.CATCH_DATE_FORMAT)
            catch_hour = catch_date.strftime("%H")

            self.data_dict[formatted_string] = float(catch_hour)
