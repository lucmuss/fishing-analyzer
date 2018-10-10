import flask
import dash

from dash.dependencies import Input, Output

from data.model import FishStatisticModel
fish_data = FishStatisticModel()

from apps.navigation import header
from apps.visualisation import environmental_data
from apps.visualisation import month_statistics

main_server = flask.Flask(__name__)

dash_app = dash.Dash(__name__, server=main_server, url_base_pathname='/visualisation/')
dash_app.config.suppress_callback_exceptions = True

dash_app.layout = header.layout


@dash_app.callback(Output('page_content', 'children'),
                   [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/visualisation/apps/environmental_data':
        return environmental_data.layout
    elif pathname == '/visualisation/apps/month_statistics':
        return month_statistics.layout
    else:
        return ""


# TODO
@main_server.route('/fish/list', methods=['GET'])
def list_fishes():
    return [1]


# TODO
@main_server.route('/fish/hello')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    dash_app.run_server(debug=True)
