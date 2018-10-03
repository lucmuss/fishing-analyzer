from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from data_model import fish_data
from app import app


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


text_description = '''The data set was collected form different kinds 
of fish catches in the river Baunach.'''

text_header = 'Visualization of Environmental Data of the River Baunach'

year_options = generate_year_options(fish_data)
default_year = '2017'

attribute_options = generate_attribute_options(fish_data)
default_attribute = 'water_temperature'

month_options = generate_month_options(fish_data)
default_month = ''

day_options = generate_day_options(fish_data)
default_day = ''

default_data_selection = fish_data.get_frame_by_year(default_year)

default_data_graph_data_series = default_data_selection[default_attribute]
default_data_graph_x_values = list(default_data_graph_data_series.index.get_values())
default_data_graph_y_values = list(default_data_graph_data_series.get_values())

default_data_graph_graph_name = "{}".format(default_attribute)
default_data_graph_graph_title = "{} {}".format(default_attribute, default_year)

layout = html.Div(children=[

    html.H2(children=text_header),

    dcc.Markdown(children=text_description),

    dcc.Link('Go to Month Statistics', href='/apps/month_statistics'),

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
                {'x': default_data_graph_x_values, 'y': default_data_graph_y_values, 'type': 'line',
                 'name': default_data_graph_graph_name},
            ],
            'layout': {
                'title': default_data_graph_graph_title
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
