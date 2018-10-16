# coding: utf-8

import datetime

import numpy

import config


def get_month_dict():
    return_dict = dict()

    for month_index in range(1, 12 + 1):
        month_string = str(month_index)
        month_name = datetime.date(2017, month_index, 1).strftime('%B')
        return_dict[month_string] = month_name

    return return_dict


def get_year_list():
    date_time_start = datetime.datetime.strptime(config.MINIMAL_SERIES_START_YEAR, "%Y-%m-%d %H:00:00")
    year_start = date_time_start.strftime("%Y")
    year_start_int = int(year_start)

    date_time_end = datetime.datetime.strptime(config.MAXIMAL_SERIES_END_YEAR, "%Y-%m-%d %H:00:00")
    year_end = date_time_end.strftime("%Y")
    year_end_int = int(year_end)

    year_range = range(year_start_int, year_end_int + 1)
    year_return_list = [str(year) for year in year_range]

    return year_return_list


def get_day_dict():
    return_dict = dict()

    for month_index in range(1, 31 + 1):
        return_dict[month_index] = month_index

    return return_dict


get_month_name = lambda month_index: config.MONTH_DICT[str(month_index)]
get_database_document = lambda fish_type, catch_date,: {"fish_type": fish_type, "catch_date": catch_date}


def attribute_to_name(attribute_name):
    attribute_list = attribute_name.split('_')

    attribute_list = [attribute.title() for attribute in attribute_list]

    attribute_title = ' '.join(attribute_list)

    return attribute_title


fish_and_attribute = lambda fish_type, attribute_name: "{}: {}".format(fish_type, attribute_name)


def strip_row(row):
    return (element.strip() for element in row)


def remove_outliers(panda_series):
    mean_value = panda_series.mean()
    std_value = panda_series.std()
    compare_factor = config.STANDARD_DEVIATION_FACTOR * std_value

    bad_index = panda_series[numpy.abs(panda_series - mean_value) >= compare_factor]
    panda_series = panda_series.drop(index=bad_index.index)

    return panda_series


def series_to_graph(panda_series):
    x_values = list(panda_series.index.get_values())
    y_values = list(panda_series.get_values())

    return x_values, y_values