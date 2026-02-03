# coding: utf-8

from typing import Any, List, Tuple

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import config
import utils
from apps.utils import (generate_attribute_options, generate_day_options,
                        generate_month_options, generate_year_options)
from data.model import ModelFactory
from mainapp import app

model_factory: ModelFactory = ModelFactory()
fish_statistic_model: Any = model_factory.statistic_model

year_options: list[dict[str, str]] = generate_year_options()
default_year: str = config.DEFAULT_YEAR

attribute_options: list[dict[str, str]] = generate_attribute_options(fish_statistic_model)
default_attribute: str = config.DEFAULT_ATTRIBUTE

month_options: list[dict[str, str]] = generate_month_options()
default_month: str = config.DEFAULT_MONTH

day_options: list[dict[str, str]] = generate_day_options()
default_day: str = config.DEFAULT_DAY

default_data_selection: Any = fish_statistic_model.get_frame_by_year(default_year)

default_data_series: Any = default_data_selection[default_attribute]

default_x_values: list[Any]
default_y_values: list[Any]
default_x_values, default_y_values = utils.series_to_graph(default_data_series)

default_name: str = utils.attribute_to_name(default_attribute)
default_title: str = utils.get_graph_name(attribute_name=default_attribute,
                                     fish_type=default_year)


def generate_line(
    x_values: List[Any] = default_x_values,
    y_values: List[Any] = default_y_values,
    name: str = default_name,
    attribute_name: str = default_attribute,
    title: str = default_title
) -> dict:
    """Generiert eine Plotly Linienfigur für Umweltdaten."
    color: Tuple[int, int, int] = config.ATTRIBUTE_COLOR_DICT[attribute_name]

    scatter: go.Scatter = go.Scatter(
        x=x_values,
        y=y_values,
        name=name,
        line=dict(color=color),
    )

    data: list[go.Scatter] = [scatter]
    layout: go.Layout = go.Layout()

    layout_dict: dict = utils.get_layout_dict(title=title)

    layout.update(layout_dict)

    figure: dict = go.Figure(data=data, layout=layout)

    return figure


layout = html.Div(children=[

    dcc.Graph(
        id='environment_data',

        figure=generate_line()
    ),

    html.Form(children=[

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3', children=[
            html.Label('Year Selection'),
            dcc.Dropdown(
                id='environment_data_year_selection',
                options=year_options,
                value=default_year
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3', children=[
            html.Label('Month Selection'),
            dcc.Dropdown(
                id='environment_data_month_selection',
                options=month_options,
                value=default_month
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3', children=[
            html.Label('Day Selection'),
            dcc.Dropdown(
                id='environment_data_day_selection',
                options=day_options,
                value=default_day
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3', children=[
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
def update_data_graph(
    year_value: str,
    month_value: str,
    day_value: str,
    attribute_name: str
) -> dict:
    """Aktualisiert den Umweltdaten-Graphen basierend auf den ausgewählten Filtern.""
    data_selection: Any = fish_statistic_model

    if year_value and month_value and day_value:
        data_selection = data_selection.get_frame_by_day(year_value, month_value, day_value)
    elif year_value and month_value:
        data_selection = data_selection.get_frame_by_month(year_value, month_value)
    elif year_value:
        data_selection = data_selection.get_frame_by_year(year_value)

    data_series: Any = data_selection[attribute_name]

    x_values: list[Any]
y_values: list[Any]
x_values, y_values = utils.series_to_graph(data_series)

    name: str = utils.attribute_to_name(attribute_name)
    title: str = utils.get_graph_name(attribute_name=attribute_name, fish_type=year_value)

    figure: dict = generate_line(x_values=x_values,
                           y_values=y_values,
                           name=name,
                           attribute_name=attribute_name,
                           title=title)

    return figure


layout = html.Div(children=[

    dcc.Graph(
        id='environment_data',

        figure=generate_line()
    ),

    html.Form(children=[

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3', children=[
            html.Label('Year Selection'),
            dcc.Dropdown(
                id='environment_data_year_selection',
                options=year_options,
                value=default_year
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3', children=[
            html.Label('Month Selection'),
            dcc.Dropdown(
                id='environment_data_month_selection',
                options=month_options,
                value=default_month
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3', children=[
            html.Label('Day Selection'),
            dcc.Dropdown(
                id='environment_data_day_selection',
                options=day_options,
                value=default_day
            ),
        ]),

        html.Div(className='form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3', children=[
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
    data_selection = fish_statistic_model

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

    figure = generate_line(x_values=x_values,
                           y_values=y_values,
                           name=name,
                           attribute_name=attribute_name,
                           title=title)

    return figure
