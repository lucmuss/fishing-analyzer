# coding: utf-8

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input
from dash.dependencies import Output
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


def generate_method_options():
    return_list = list()

    for method in config.STATISTIC_METHODS:
        return_list.append({'label': method.title(), 'value': method})

    return return_list


def generate_attribute_options(fish_data):
    return_list = list()

    for attribute in fish_data.plotable_attributes:
        name = utils.attribute_to_name(attribute)
        return_list.append({'label': name, 'value': attribute})

    return return_list


def extract_data_values(year, attribute, method, month_statistics):
    data_dict = month_statistics[(year, attribute)]

    x_values = [config.get_month_name(month_index) for month_index in data_dict.keys()]
    y_values = [value[method] for key, value in data_dict.items()]

    return x_values, y_values


month_statistics = fish_data.month_statistics

year_options = generate_year_options()
default_year = config.DEFAULT_YEAR

method_options = generate_method_options()
default_method = config.DEFAULT_STATISTIC_METHOD

attribute_options = generate_attribute_options(fish_data)
default_attribute = config.DEFAULT_ATTRIBUTE

default_name = utils.attribute_to_name(default_attribute)
default_title = utils.get_graph_name(attribute_name=default_attribute,
                                     fish_type=default_year)

default_x_values, default_y_values = extract_data_values(default_year, default_attribute,
                                                         default_method,
                                                         month_statistics)


def generate_bar(x_values=default_x_values, y_values=default_y_values,
                 name=default_name,
                 title=default_title):
    bar = plotly.graph_objs.Bar(
        x=x_values,
        y=y_values,
        name=name
    )

    data = [bar]
    layout = plotly.graph_objs.Layout()

    layout_dict = utils.get_layout_dict(title=title)

    layout.update(layout_dict)

    figure = plotly.graph_objs.Figure(data=data, layout=layout)

    return figure


layout = html.Div(children=[

    html.Div(children=[

        html.Label('Year Selection'),
        dcc.Dropdown(
            id='month_statistics_year_selection',
            options=year_options,
            value=default_year
        ),

        html.Label('Attribute Selection'),
        dcc.Dropdown(
            id='month_statistics_attribute_selection',
            options=attribute_options,
            value=default_attribute
        ),

        html.Label('Method Selection'),
        dcc.Dropdown(
            id='month_statistics_method_selection',
            options=method_options,
            value=default_method
        ),

    ]),

    dcc.Graph(
        id='month_statistics',

        figure=generate_bar()
    )

])


@app.callback(
    Output('month_statistics', 'figure'),
    [Input('month_statistics_year_selection', 'value'),
     Input('month_statistics_attribute_selection', 'value'),
     Input('month_statistics_method_selection', 'value')])
def update_month_statistics(year_value, attribute_name, method):
    x_values, y_values = extract_data_values(year_value, attribute_name, method, month_statistics)

    name = utils.attribute_to_name(attribute_name)
    title = utils.get_graph_name(attribute_name=attribute_name, fish_type=year_value)

    figure = generate_bar(x_values=x_values, y_values=y_values,
                          name=name, title=title)

    return figure
