# coding: utf-8

import config
from data.environment.base_attribute import BaseAttribute


class CatchMonth(BaseAttribute):
    attribute_name = 'fish_catch_month'

    def __init__(self, database_model=None):
        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               )

        self.__read(fish_list=database_model.fish_list)

    def __read(self, fish_list):
        for document in fish_list:
            catch_date = document['catch_date']

            formatted_string = catch_date.strftime(config.CATCH_DATE_FORMAT)

            catch_day = catch_date.strftime("%d")
            catch_month = catch_date.strftime("%m")

            catch_day_float = (float(catch_day) / 31.0) * 1.0
            catch_month_float = (float(catch_month) / 12.0) * 12.0

            self.data_dict[formatted_string] = catch_month_float + catch_day_float
