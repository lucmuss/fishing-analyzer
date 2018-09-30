import dash
import flask
import os

import dash_core_components as dcc
import dash_html_components as html
from flask import send_from_directory

from data_aggregation import fish_data

custom_stylesheet = ['/static/custom_style.css']

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, external_stylesheets=custom_stylesheet)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

text_description = '''The data set was collected form different kinds 
of fish catches in the river Baunach.'''


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


def generate_graphs(fish_data):
    fish_year_dict = fish_data.get_year_dict()

    # data_2017_air_temperature = fish_year_dict['2017']['air_temperature']
    data_2016_water_temperature = fish_year_dict['2016']['water_temperature']

    # graph_2017 = graph_by_series(data_2017_air_temperature, '2017', 'air_temperature')
    graph_2016 = graph_by_series(data_2016_water_temperature, '2016', 'water_temperature')

    return graph_2016


def graph_by_series(data_series, year, attribute):
    data_series = data_series

    x_values = list(data_series.index.get_values())
    y_values = list(data_series.get_values())

    graph_id = "{}_{}".format(year, attribute)
    graph_name = "{}".format(attribute)

    attribute_title = attribute.title().replace('_', ' ')
    year_title = year.title()

    graph_title = "{} {}".format(attribute_title, year_title)

    new_graph = dcc.Graph(
        id=graph_id,

        figure={
            'data': [
                {'x': x_values, 'y': y_values, 'type': 'line', 'name': graph_name},
            ],
            'layout': {
                'title': graph_title
            }
        }
    )
    return new_graph


app.layout = html.Div(children=[

    html.Link(
        rel='stylesheet',
        href='/static/custom_style.css'
    ),

    html.H2(children='Visualization of Environmental Data of the River Baunach',
            style={'className': 'superclass', 'textAlign': 'center'}),

    dcc.Markdown(children=text_description),

    html.Div(children=[

        generate_graphs(fish_data)

    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
