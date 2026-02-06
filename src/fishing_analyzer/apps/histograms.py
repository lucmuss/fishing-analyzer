from typing import Any, cast

import plotly.graph_objs as go
from dash import Input, Output, dcc, html

from fishing_analyzer import config, utils
from fishing_analyzer.apps.utils import generate_attribute_options, generate_fish_type_options
from fishing_analyzer.data.model import ModelFactory
from fishing_analyzer.mainapp import app

model_factory: ModelFactory = ModelFactory()
fish_frame_model: Any = model_factory.fish_frame_model

fish_options: list[dict[str, str]] = generate_fish_type_options(fish_model=fish_frame_model)
default_fish_type: str = config.DEFAULT_FISH_TYPE

attribute_options: list[dict[str, str]] = generate_attribute_options(fish_frame_model)
default_attribute: str = config.DEFAULT_ATTRIBUTE

default_data_selection: Any = fish_frame_model.get_fish_frame(default_fish_type)

default_data_series: Any = default_data_selection[default_attribute]

default_y_values: list[float]
default_x_values: list[float]
default_y_values, default_x_values = utils.safe_series_to_graph(default_data_series)

default_name: str = utils.attribute_to_name(default_attribute)

default_title: str = utils.get_graph_name(
    attribute_name=default_attribute, fish_type=default_fish_type
)


def generate_histogram(
    x_values=default_x_values,
    name=default_name,
    attribute_name=default_attribute,
    title=default_title,
):
    color = config.ATTRIBUTE_COLOR_DICT[attribute_name]

    histogram = go.Histogram(
        x=x_values,
        nbinsx=config.HISTOGRAM_BINS,
        name=name,
        marker={"color": color},
    )

    data = [histogram]
    layout = go.Layout()

    layout_dict = utils.get_layout_dict(title=title)

    layout.update(layout_dict)

    figure = go.Figure(data=data, layout=layout)

    return figure


layout = html.Div(
    children=[
        dcc.Graph(id="fish_histograms", figure=generate_histogram()),
        html.Form(
            children=[
                html.Div(
                    className="form-group float-left col-sm-6",
                    children=[
                        html.Label("Fish Selection"),
                        dcc.Dropdown(
                            id="fish_histograms_fish_selection",
                            options=cast(Any, fish_options),
                            value=default_fish_type,
                        ),
                    ],
                ),
                html.Div(
                    className="form-group float-left col-sm-6",
                    children=[
                        html.Label("Attribute Selection"),
                        dcc.Dropdown(
                            id="fish_histograms_attribute_selection",
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
    Output("fish_histograms", "figure"),
    [
        Input("fish_histograms_fish_selection", "value"),
        Input("fish_histograms_attribute_selection", "value"),
    ],
)
def update_data_graph(fish_type, attribute_name):
    data_selection = fish_frame_model

    if fish_type:
        data_selection = data_selection.get_fish_frame(fish_type)

    data_series = data_selection[attribute_name]

    y_values, x_values = utils.safe_series_to_graph(data_series)

    name = utils.attribute_to_name(attribute_name)
    title = utils.get_graph_name(attribute_name=attribute_name, fish_type=fish_type)

    figure = generate_histogram(
        x_values=x_values, title=title, attribute_name=attribute_name, name=name
    )

    return figure
