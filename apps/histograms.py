# coding: utf-8

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly
import utils
import config
from mainapp import app
from data.model import fish_frame_model

fish_data = fish_frame_model


def generate_attribute_options(fish_data):
    return_list = list()

    for attribute in fish_data.plotable_attributes:
        name = utils.attribute_to_name(attribute)
        return_list.append({'label': name, 'value': attribute})

    return return_list


def generate_fish_options(fish_model):
    return_list = list()

    for fish_type in config.FISH_TYPES:
        fish_frame = fish_model.get_fish_frame(fish_type)

        if utils.is_valid_fish_frame(fish_frame):
            return_list.append({'label': fish_type, 'value': fish_type})

    return return_list


fish_options = generate_fish_options(fish_model=fish_data)
default_fishtype = config.DEFAULT_FISH

attribute_options = generate_attribute_options(fish_data)
default_attribute = config.DEFAULT_ATTRIBUTE

default_data_selection = fish_data.get_fish_frame(default_fishtype)

default_data_series = default_data_selection[default_attribute]

default_y_values, default_x_values = utils.safe_series_to_graph(default_data_series)

default_name = utils.attribute_to_name(default_attribute)

default_title = utils.get_graph_name(attribute_name=default_attribute,
                                     fish_type=default_fishtype)


def generate_histogram(x_values=default_x_values,
                       name=default_name,
                       title=default_title):
    histogram = plotly.graph_objs.Histogram(
        x=x_values,
        nbinsx=config.HISTOGRAM_BINS,
        name=name,
    )

    data = [histogram]
    layout = plotly.graph_objs.Layout()

    layout_dict = utils.get_layout_dict(title=title)

    layout.update(layout_dict)

    figure = plotly.graph_objs.Figure(data=data, layout=layout)

    return figure


layout = html.Div(children=[

    dcc.Graph(
        id='fish_histograms',
        figure=generate_histogram()
    ),

    html.Form(children=[

        html.Div(className='form-group float-left col-sm-6', children=[
            html.Label('Fish Selection'),
            dcc.Dropdown(
                id='fish_histograms_fish_selection',
                options=fish_options,
                value=default_fishtype
            ),
        ]),

        html.Div(className='form-group float-left col-sm-6', children=[
            html.Label('Attribute Selection'),
            dcc.Dropdown(
                id='fish_histograms_attribute_selection',
                options=attribute_options,
                value=default_attribute
            ),
        ]),

    ]),

])


@app.callback(
    Output('fish_histograms', 'figure'),
    [Input('fish_histograms_fish_selection', 'value'),
     Input('fish_histograms_attribute_selection', 'value')])
def update_data_graph(fish_type, attribute_name):
    data_selection = fish_data

    if fish_type:
        data_selection = data_selection.get_fish_frame(fish_type)

    data_series = data_selection[attribute_name]

    y_values, x_values = utils.safe_series_to_graph(data_series)

    name = utils.attribute_to_name(attribute_name)
    title = utils.get_graph_name(attribute_name=attribute_name, fish_type=fish_type)

    figure = generate_histogram(x_values=x_values, title=title, name=name)

    return figure
