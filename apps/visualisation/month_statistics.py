from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

import config
from index import fish_data
from index import dash_app

from apps.visualisation.environmental_data import generate_year_options
from apps.visualisation.environmental_data import generate_attribute_options


def extract_data_values(year, attribute, month_statistics):
    data_dict = month_statistics[(year, attribute)]

    x_values = [config.get_month_name(month_index) for month_index in data_dict.keys()]
    y_values = [mean_value for mean_value, sum_values in data_dict.values()]

    return x_values, y_values


text_description = '''The data set was collected form different kinds 
of fish catches in the river Baunach.'''

text_header = 'Visualization of the Month Statistics of the River Baunach'

month_statistics = fish_data.month_statistics

default_graph_name = "{}".format(config.DEFAULT_ATTRIBUTE)
default_graph_title = "{} {}".format(config.DEFAULT_ATTRIBUTE, config.DEFAULT_YEAR)

year_options = generate_year_options()
default_year = config.DEFAULT_YEAR

attribute_options = generate_attribute_options(fish_data)
default_attribute = config.DEFAULT_ATTRIBUTE

default_x_values, default_y_values = extract_data_values(default_year, default_attribute, month_statistics)

layout = html.Div(children=[

    html.H2(children=text_header),

    dcc.Markdown(children=text_description),

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

    ]),

    dcc.Graph(
        id='month_statistics',

        figure={
            'data': [
                {'x': default_x_values, 'y': default_y_values,
                 'type': 'bar',
                 'name': default_graph_name},
            ],
            'layout': {
                'title': default_graph_title
            }
        }
    )

])


@dash_app.callback(
    Output('month_statistics', 'figure'),
    [Input('month_statistics_year_selection', 'value'),
     Input('month_statistics_attribute_selection', 'value')])
def update_month_statistics(year_value, attribute_name):
    x_values, y_values = extract_data_values(year_value, attribute_name, month_statistics)

    graph_name = "{}".format(attribute_name)

    attribute_title = attribute_name.title().replace('_', ' ')
    year_title = year_value.title()

    graph_title = "{} {}".format(attribute_title, year_title)

    return_figure = {
        'data': [
            {'x': x_values, 'y': y_values, 'type': 'bar', 'name': graph_name},
        ],
        'layout': {
            'title': graph_title
        }
    }

    return return_figure
