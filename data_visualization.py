import dash
import flask
import os
import dash

import dash_core_components as dcc
import dash_html_components as html
from flask import send_from_directory

from data_model import fish_data

custom_stylesheet = ['/static/custom_style.css']

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, external_stylesheets=custom_stylesheet)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

text_description = '''The data set was collected form different kinds 
of fish catches in the river Baunach.'''


def generate_year_options(fish_data):
    return_list = list()

    for year in fish_data.get_year_list():
        year_name = 'Year: {}'.format(year.title())
        return_list.append({'label': year_name, 'value': str(year)})

    return return_list


def generate_attribute_options(fish_data):
    return_list = list()

    for attribute in fish_data.get_plotable_attributes():
        attribute_name = 'Attribute: {}'.format(attribute.title().replace('_', ' '))
        return_list.append({'label': attribute_name, 'value': str(attribute)})

    return return_list


def generate_month_options(fish_data):
    return_list = list()

    for month_index, month_name in fish_data.get_month_dict().items():
        month_name_label = 'Monat: {}'.format(month_name.title())
        return_list.append({'label': month_name_label, 'value': str(month_index)})

    return return_list


def generate_day_options(fish_data):
    return_list = list()

    for day_index, day_value in fish_data.get_day_dict().items():
        month_name_label = 'Tag: {}'.format(day_index)
        return_list.append({'label': month_name_label, 'value': str(day_index)})

    return return_list


year_options = generate_year_options(fish_data)
default_year = '2017'

attribute_options = generate_attribute_options(fish_data)
default_attribute = 'water_temperature'

month_options = generate_month_options(fish_data)
default_month = ''

day_options = generate_day_options(fish_data)
default_day = ''

default_data_selection = fish_data.get_frame_by_year(default_year)

default_data_series = default_data_selection[default_attribute]
default_x_values = list(default_data_series.index.get_values())
default_y_values = list(default_data_series.get_values())

default_graph_name = "{}".format(default_attribute)
default_graph_title = "{} {}".format(default_attribute, default_year)

app.layout = html.Div(children=[

    html.H2(children='Visualization of Environmental Data of the River Baunach',
            style={'className': 'superclass'}),

    dcc.Markdown(children=text_description),

    html.Label('Year Selection'),
    dcc.Dropdown(
        id='year_selection',
        options=year_options,
        value=default_year
    ),

    html.Label('Month Selection'),
    dcc.Dropdown(
        id='month_selection',
        options=month_options,
        value=default_month
    ),

    html.Label('Day Selection'),
    dcc.Dropdown(
        id='day_selection',
        options=day_options,
        value=default_day
    ),

    html.Label('Attribute Selection'),
    dcc.Dropdown(
        id='attribute_selection',
        options=attribute_options,
        value=default_attribute
    ),

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


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


@app.callback(
    dash.dependencies.Output('data_graph', 'figure'),
    [dash.dependencies.Input('year_selection', 'value'),
     dash.dependencies.Input('month_selection', 'value'),
     dash.dependencies.Input('day_selection', 'value'),
     dash.dependencies.Input('attribute_selection', 'value')])
def update_graph(year_value, month_value, day_value, attribute_name):
    data_selection = fish_data

    if year_value and month_value and day_value:
        data_selection = data_selection.get_frame_by_day(year_value, month_value, day_value)
    elif year_value and month_value:
        data_selection = data_selection.get_frame_by_month(year_value, month_value)
    elif year_value:
        data_selection = data_selection.get_frame_by_year(year_value)

    data_series = data_selection[attribute_name]

    x_values = list(data_series.index.get_values())
    y_values = list(data_series.get_values())

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
