# coding: utf-8

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly

import utils
import config
from mainapp import app
from data.model import statistic_model

fish_data = statistic_model


def generate_year_options():
    return_list = list()

    for year in config.YEAR_RANGE:
        return_list.append({'label': year, 'value': year})

    return return_list


def generate_attribute_options(fish_data):
    return_list = list()

    for attribute in fish_data.plotable_attributes:
        name = utils.attribute_to_name(attribute)
        return_list.append({'label': name, 'value': attribute})

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


year_options = generate_year_options()
default_year = config.DEFAULT_YEAR

attribute_options = generate_attribute_options(fish_data)
default_attribute = config.DEFAULT_ATTRIBUTE

month_options = generate_month_options()
default_month = config.DEFAULT_MONTH

day_options = generate_day_options()
default_day = config.DEFAULT_DAY

default_data_selection = fish_data.get_frame_by_year(default_year)

default_data_series = default_data_selection[default_attribute]

default_x_values, default_y_values = utils.series_to_graph(default_data_series)

default_name = utils.attribute_to_name(default_attribute)
default_title = utils.get_graph_name(attribute_name=default_attribute,
                                     fish_type=default_year)


def generate_line(x_values=default_x_values, y_values=default_y_values,
                  name=default_name,
                  title=default_title):
    scatter = plotly.graph_objs.Scatter(
        x=x_values,
        y=y_values,
        name=name
    )

    data = [scatter]
    layout = plotly.graph_objs.Layout()

    layout_dict = utils.get_layout_dict(title=title)

    layout.update(layout_dict)

    figure = plotly.graph_objs.Figure(data=data, layout=layout)

    return figure


layout = html.Div(children=[

    dcc.Graph(
        id='environment_data',

        figure=generate_line()
    ),

    html.Form(children=[

        html.Div(className='form-group float-left col-sm-6', children=[
            html.Label('Year Selection'),
            dcc.Dropdown(
                id='environment_data_year_selection',
                options=year_options,
                value=default_year
            ),
        ]),

        html.Div(className='form-group float-left col-sm-6', children=[
            html.Label('Month Selection'),
            dcc.Dropdown(
                id='environment_data_month_selection',
                options=month_options,
                value=default_month
            ),
        ]),

        html.Div(className='form-group float-left col-sm-6', children=[
            html.Label('Day Selection'),
            dcc.Dropdown(
                id='environment_data_day_selection',
                options=day_options,
                value=default_day
            ),
        ]),

        html.Div(className='form-group float-left col-sm-6', children=[
            html.Label('Attribute Selection'),
            dcc.Dropdown(
                id='environment_data_attribute_selection',
                options=attribute_options,
                value=default_attribute
            ),
        ]),

    ]),

])


@app.callback(
    Output('environment_data', 'figure'),
    [Input('environment_data_year_selection', 'value'),
     Input('environment_data_month_selection', 'value'),
     Input('environment_data_day_selection', 'value'),
     Input('environment_data_attribute_selection', 'value')])
def update_data_graph(year_value, month_value, day_value, attribute_name):
    data_selection = fish_data

    if year_value and month_value and day_value:
        data_selection = data_selection.get_frame_by_day(year_value, month_value, day_value)
    elif year_value and month_value:
        data_selection = data_selection.get_frame_by_month(year_value, month_value)
    elif year_value:
        data_selection = data_selection.get_frame_by_year(year_value)

    data_series = data_selection[attribute_name]

    x_values, y_values = utils.series_to_graph(data_series)

    name = utils.attribute_to_name(attribute_name)
    title = utils.get_graph_name(attribute_name=attribute_name, fish_type=year_value)

    figure = generate_line(x_values=x_values, y_values=y_values,
                           name=name,
                           title=title)

    return figure
