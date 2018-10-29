# coding: utf-8

import config
import utils


def generate_attribute_options(fish_model):
    return_list = list()

    for attribute in fish_model.plotable_attributes:
        name = utils.attribute_to_name(attribute)
        return_list.append({'label': name, 'value': attribute})

    return return_list


def generate_fish_type_options(fish_model):
    return_list = list()

    for fish_type in config.FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if utils.is_valid_fish_frame(fish_frame):
            return_list.append({'label': fish_type, 'value': fish_type})

    return return_list


def generate_year_options():
    return_list = list()

    for year in config.YEAR_RANGE:
        return_list.append({'label': year, 'value': year})

    return return_list


def generate_month_options():
    return_list = list()

    for month_index, month_name in config.MONTH_NAME_DICT.items():
        return_list.append({'label': month_name.title(), 'value': month_index})

    return return_list


def generate_day_options():
    return_list = list()

    for day_index, day_value in config.MONTH_DAYS_DICT.items():
        return_list.append({'label': str(day_index), 'value': str(day_index)})

    return return_list


def generate_method_options():
    return_list = list()

    for method in config.STATISTIC_METHODS:
        return_list.append({'label': method.title(), 'value': method})

    return return_list
