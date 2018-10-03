from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from data_model import fish_data
from dash_apps.environmental_data import text_description
from dash_apps.environmental_data import default_year
from dash_apps.environmental_data import default_attribute
from dash_apps.environmental_data import year_options
from dash_apps.environmental_data import attribute_options
from app import app

month_dict = fish_data.get_month_dict()
get_month_name = lambda month_index: month_dict[str(month_index)]


def exract_data_values(year, attribute, month_statistics):
    data_dict = month_statistics[(year, attribute)]

    x_values = [get_month_name(month_index) for month_index in data_dict.keys()]
    y_values = [mean_value for mean_value, sum_values in data_dict.values()]

    return x_values, y_values


month_statistics = fish_data.get_month_statistics()

default_month_statistics_graph_name = "{}".format(default_attribute)
default_month_statistics_graph_title = "{} {}".format(default_attribute, default_year)

default_month_statistics_x_values, default_month_statistics_y_values = exract_data_values(default_year,
                                                                                          default_attribute,
                                                                                          month_statistics)

layout = html.Div(children=[

    html.H2(children='Visualization of Environmental Data of the River Baunach'),

    dcc.Markdown(children=text_description),

    dcc.Link('Go to Environmental Data', href='/apps/environmental_data'),

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
                {'x': default_month_statistics_x_values, 'y': default_month_statistics_y_values,
                 'type': 'bar',
                 'name': default_month_statistics_graph_name},
            ],
            'layout': {
                'title': default_month_statistics_graph_title
            }
        }
    )

])


@app.callback(
    Output('month_statistics', 'figure'),
    [Input('month_statistics_year_selection', 'value'),
     Input('month_statistics_attribute_selection', 'value')])
def update_month_statistics(year_value, attribute_name):
    x_values, y_values = exract_data_values(year_value, attribute_name, month_statistics)

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
