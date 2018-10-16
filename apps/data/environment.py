# coding: utf-8

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import config
from mainapp import app
from utils import series_to_graph
from data.model import fish_statistic_model

fish_data = fish_statistic_model

def generate_year_options():
    return_list = list()

    for year in config.YEAR_LIST:
        year_name = 'Year: {}'.format(year.title())
        return_list.append({'label': year_name, 'value': str(year)})

    return return_list


def generate_attribute_options(fish_data):
    return_list = list()

    for attribute in fish_data.plotable_attributes:
        attribute_name = 'Attribute: {}'.format(attribute.title().replace('_', ' '))
        return_list.append({'label': attribute_name, 'value': str(attribute)})

    return return_list


def generate_month_options():
    return_list = list()

    for month_index, month_name in config.MONTH_DICT.items():
        month_name_label = 'Monat: {}'.format(month_name.title())
        return_list.append({'label': month_name_label, 'value': str(month_index)})

    return return_list


def generate_day_options():
    return_list = list()

    for day_index, day_value in config.MONTH_DAYS_DICT.items():
        month_name_label = 'Tag: {}'.format(day_index)
        return_list.append({'label': month_name_label, 'value': str(day_index)})

    return return_list


text_description = '''The data set was collected form different kinds 
of fish catches in the river Baunach.'''

text_header = 'Visualization of Environmental Data of the River Baunach'

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

default_x_values, default_y_values = series_to_graph(default_data_series)

default_graph_name = "{}".format(default_attribute)
default_graph_title = "{} {}".format(default_attribute, default_year)

layout = html.Div(children=[

    html.H2(children=text_header),

    dcc.Markdown(children=text_description),

    html.Div(children=[

        html.Label('Year Selection'),
        dcc.Dropdown(
            id='data_graph_year_selection',
            options=year_options,
            value=default_year
        ),

        html.Label('Month Selection'),
        dcc.Dropdown(
            id='data_graph_month_selection',
            options=month_options,
            value=default_month
        ),

        html.Label('Day Selection'),
        dcc.Dropdown(
            id='data_graph_day_selection',
            options=day_options,
            value=default_day
        ),

        html.Label('Attribute Selection'),
        dcc.Dropdown(
            id='data_graph_attribute_selection',
            options=attribute_options,
            value=default_attribute
        ),

    ]),

    dcc.Graph(
        id='data_graph',

        figure={
            'data': [
                {'x': default_x_values, 'y': default_y_values, 'type': 'line',
                 'name': default_graph_name},
            ],
            'layout': {
                'title': default_graph_title
            }
        }
    )

])


@app.callback(
    Output('data_graph', 'figure'),
    [Input('data_graph_year_selection', 'value'),
     Input('data_graph_month_selection', 'value'),
     Input('data_graph_day_selection', 'value'),
     Input('data_graph_attribute_selection', 'value')])
def update_data_graph(year_value, month_value, day_value, attribute_name):
    data_selection = fish_data

    if year_value and month_value and day_value:
        data_selection = data_selection.get_frame_by_day(year_value, month_value, day_value)
    elif year_value and month_value:
        data_selection = data_selection.get_frame_by_month(year_value, month_value)
    elif year_value:
        data_selection = data_selection.get_frame_by_year(year_value)

    data_series = data_selection[attribute_name]

    x_values, y_values = series_to_graph(data_series)

    graph_name = "{}".format(attribute_name)

    attribute_title = attribute_name.title().replace('_', ' ')
    year_title = year_value.title()

    graph_title = "{} {}".format(attribute_title, year_title)

    return_figure = {
        'data': [
            {'x': x_values, 'y': y_values, 'type': 'line', 'name': graph_name},
        ],
        'layout': {
            'title': graph_title
        }
    }

    return return_figure
