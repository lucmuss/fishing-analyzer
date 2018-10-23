# coding: utf-8

import config
from data.environment.base_attribute import BaseAttribute


class FishType(BaseAttribute):
    attribute_name = 'fish_type'

    def __init__(self, database_model=None):
        BaseAttribute.__init__(self,
                               attribute_name=self.attribute_name,
                               )

        self.__read(fish_list=database_model.fish_list)

    def __read(self, fish_list):
        for document in fish_list:
            catch_date = document['catch_date']
            fish_type = document['fish_type']

            formatted_string = catch_date.strftime(config.CATCH_DATE_FORMAT)

            self.data_dict[formatted_string] = fish_type
