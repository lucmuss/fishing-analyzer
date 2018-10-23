# coding: utf-8

import numpy

import config


def clean_series(attribute_series):
    nan_series = attribute_series.replace([numpy.inf, -numpy.inf], numpy.nan)
    clean_series = nan_series.fillna(0.0)
    return clean_series


def get_database_document(fish_type, catch_date, dataset_id):
    return_dict = dict(config.DATABASE_DOCUMENT)
    keys = list(return_dict.keys())

    return_dict[keys[0]] = fish_type
    return_dict[keys[1]] = catch_date
    return_dict[keys[2]] = dataset_id

    return return_dict


def attribute_to_name(attribute_name):
    return attribute_name.title().replace('_', ' ')


def fishtype_to_name(fishtype):
    return fishtype


def get_graph_name(attribute_name, fish_type):
    fishtype = fishtype_to_name(fish_type)
    attribute = attribute_to_name(attribute_name)

    return "{} - {}".format(fishtype, attribute)


def is_plotable(series):
    return series.dtype == 'float64'


def fish_and_attribute(fish_type, attribute_name):
    return "{} -> {}".format(fish_type, attribute_name)


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


def safe_series_to_graph(panda_series):
    clean = clean_series(panda_series)
    return series_to_graph(clean)


def validate_row(row, station):
    return len(row) >= 5 and station == "282"


def validate_water_row(row):
    return len(row) >= 3 and row[2] == "Rohdaten"


def get_layout_dict(title='Default', x_title='Werte', y_title='Anzahl', height=config.DIAGRAM_HEIGTH,
                    width=config.DIAGRAM_WIDTH):
    return_dict = {
        'title': title,
        'xaxis': dict(
            title=x_title
        ),
        'yaxis': dict(
            title=y_title
        ),
        'bargap': 0.1,
        'height': height,
        'width': width
    }
    return return_dict


def is_valid_fish_frame(data_frame):
    return data_frame.size >= config.MINIMAL_CATCHED_FISHES
