from typing import Any, cast

import plotly.graph_objs as go
from dash import Input, Output, dcc, html

from fishing_analyzer import config, utils
from fishing_analyzer.apps.utils import (
    generate_attribute_options,
    generate_day_options,
    generate_month_options,
    generate_year_options,
)
from fishing_analyzer.data.model import ModelFactory
from fishing_analyzer.mainapp import app

model_factory = ModelFactory()
fish_statistic_model = model_factory.statistic_model

year_options = generate_year_options()
month_options = generate_month_options()
day_options = generate_day_options()
attribute_options = generate_attribute_options(fish_statistic_model)

default_year = config.DEFAULT_YEAR
default_month = config.DEFAULT_MONTH
default_day = config.DEFAULT_DAY
default_attribute = config.DEFAULT_ATTRIBUTE

default_data_selection = fish_statistic_model.get_frame_by_year(default_year)
default_data_series = default_data_selection[default_attribute]
default_x_values, default_y_values = utils.series_to_graph(default_data_series)
default_name = utils.attribute_to_name(default_attribute)
default_title = utils.get_graph_name(attribute_name=default_attribute, fish_type=default_year)


def generate_line(
    x_values: list[Any] = default_x_values,
    y_values: list[Any] = default_y_values,
    name: str = default_name,
    attribute_name: str = default_attribute,
    title: str = default_title,
) -> go.Figure:
    color = config.ATTRIBUTE_COLOR_DICT[attribute_name]
    scatter = go.Scatter(
        x=x_values,
        y=y_values,
        name=name,
        line={"color": color},
    )

    layout = go.Layout()
    layout.update(utils.get_layout_dict(title=title))
    return go.Figure(data=[scatter], layout=layout)


layout = html.Div(
    children=[
        dcc.Graph(id="environment_data", figure=generate_line()),
        html.Form(
            children=[
                html.Div(
                    className="form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3",
                    children=[
                        html.Label("Year Selection"),
                        dcc.Dropdown(
                            id="environment_data_year_selection",
                            options=cast(Any, year_options),
                            value=default_year,
                        ),
                    ],
                ),
                html.Div(
                    className="form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3",
                    children=[
                        html.Label("Month Selection"),
                        dcc.Dropdown(
                            id="environment_data_month_selection",
                            options=cast(Any, month_options),
                            value=default_month,
                        ),
                    ],
                ),
                html.Div(
                    className="form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3",
                    children=[
                        html.Label("Day Selection"),
                        dcc.Dropdown(
                            id="environment_data_day_selection",
                            options=cast(Any, day_options),
                            value=default_day,
                        ),
                    ],
                ),
                html.Div(
                    className="form-group float-left col-xs-12 col-sm-6 col-md-4 col-lg-3",
                    children=[
                        html.Label("Attribute Selection"),
                        dcc.Dropdown(
                            id="environment_data_attribute_selection",
                            options=cast(Any, attribute_options),
                            value=default_attribute,
                        ),
                    ],
                ),
            ]
        ),
    ]
)


@app.callback(
    Output("environment_data", "figure"),
    [
        Input("environment_data_year_selection", "value"),
        Input("environment_data_month_selection", "value"),
        Input("environment_data_day_selection", "value"),
        Input("environment_data_attribute_selection", "value"),
    ],
)
def update_data_graph(
    year_value: str,
    month_value: str,
    day_value: str,
    attribute_name: str,
) -> go.Figure:
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

    return generate_line(
        x_values=x_values,
        y_values=y_values,
        name=name,
        attribute_name=attribute_name,
        title=title,
    )
