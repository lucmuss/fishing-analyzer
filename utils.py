# coding: utf-8

import datetime

import numpy

import config


def get_month_name_dict():
    return_dict = dict()

    for month_index in range(1, 12 + 1):
        month_string = str(month_index)
        month_name = datetime.date(2017, month_index, 1).strftime('%B')
        return_dict[month_string] = month_name

    return return_dict


def get_year_range():
    date_time_start = datetime.datetime.strptime(config.MINIMAL_BEGIN_DATE, "%Y-%m-%d %H:00:00")
    year_start = date_time_start.strftime("%Y")
    year_start_int = int(year_start)

    date_time_end = datetime.datetime.strptime(config.MAXIMAL_END_DATE, "%Y-%m-%d %H:00:00")
    year_end = date_time_end.strftime("%Y")
    year_end_int = int(year_end)

    year_range = range(year_start_int, year_end_int + 1)
    year_return_list = [str(year) for year in year_range]

    return year_return_list


def get_month_days_dict():
    return_dict = dict()

    for month_index in range(1, 31 + 1):
        return_dict[month_index] = month_index

    return return_dict


def get_month_name(month_index):
    return config.MONTH_NAME_DICT[str(month_index)]


def get_database_document(fish_type, catch_date, dataset_id):
    return_dict = dict(config.DATABASE_DOCUMENT)
    keys = list(return_dict.keys())

    return_dict[keys[0]] = fish_type
    return_dict[keys[1]] = catch_date
    return_dict[keys[2]] = dataset_id

    return return_dict


def attribute_to_name(attribute_name):
    attribute_list = attribute_name.split('_')

    attribute_list = [attribute.title() for attribute in attribute_list]

    attribute_title = ' '.join(attribute_list)

    return attribute_title


def is_plotable(series):
    return (series.dtype == 'float64')


def fish_and_attribute(fish_type, attribute_name):
    return "{}: {}".format(fish_type, attribute_name)


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


def validate_row(row, station):
    return len(row) >= 5 and station == "282"


def validate_water_row(row):
    return len(row) >= 3 and row[2] == "Rohdaten"
